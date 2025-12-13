import os
import math
low_score = -1000000000000.0

def build_learning_base(path_sorted: str):
    """Builds the learning base by analyzing files already classified by theme
    Parameters
    ----------
    path_sorted: path to the 'sorted' folder containing one subfolder per theme, where each subfolder contains
    text files used as learning examples (str)

    Returns
    ----------
    theme_word_counts: dictionary where each key is a theme, and the value is a dictionary associating
        each unique word with the number of files in the theme in which this word appears (dict)
    files_per_theme: dictionary where each key is a theme, and the value is the
    total number of files present in the theme folder (dict)
    """

    theme_word_counts = {}
    files_per_theme = {}

    if not os.path.isdir(path_sorted):
        return theme_word_counts, files_per_theme

    themes = os.listdir(path_sorted)

    for theme in themes:
        theme_path = path_sorted + "/" + theme

        if os.path.isdir(theme_path):

            theme_word_counts[theme] = {}
            files_per_theme[theme] = 0

            files = os.listdir(theme_path)

            for filename in files:
                file_path = theme_path + "/" + filename

                if os.path.isfile(file_path):
                    
                    files_per_theme[theme] = files_per_theme[theme] + 1
                    
                    f = open(file_path, "r")
                    text = f.read()
                    f.close()

                    text = text.lower()

                    punctuation = [".", ",", "!", "?", ":", ";", "(", ")", '"', "'"]
                    for p in punctuation:
                        text = text.replace(p, " ")

                    words = text.split()

                    unique_words = []
                    for w in words:
                        if w not in unique_words:
                            unique_words.append(w)
                    
                    for w in unique_words:
                        if w not in theme_word_counts[theme]:
                            theme_word_counts[theme][w] = 1
                        else:
                            theme_word_counts[theme][w] = theme_word_counts[theme][w] + 1

    return theme_word_counts, files_per_theme

def compute_word_probabilities(theme_word_counts: dict, files_per_theme: dict) -> dict:
    """Computes the conditional probabilities P(word | theme) for each word and each theme
    Parameters
    ----------
        theme_word_counts: dictionary where each theme is associated with a dictionary
        {word: number of files in the theme containing this word} (dict)
        files_per_theme: dictionary associating each theme with the total number of learning files
        available for that theme (dict)

    Returns
    ----------
        word_probabilities: dictionary where each theme is associated with a dictionary
        {word:probability of seeing this word in a file of this theme},
    """

    word_probabilities = {}

    for theme in theme_word_counts:
        word_probabilities[theme] = {}
        total_files = files_per_theme[theme]

        for word in theme_word_counts[theme]:
            count = theme_word_counts[theme][word]

            probability = (count + 1) / (total_files + 1)

            word_probabilities[theme][word] = probability

    return word_probabilities

def extract_words_from_file(file_path: str) -> list:
    """Extracts the list of unique words present in a text file
    Parameters
    ----------
        
    Returns
    ----------
    unique_words: list containing each word that appears at least once in the file (list)
    """

    if not os.path.isfile(file_path):
        return []

    f = open(file_path, "r")
    text = f.read()
    f.close()

    text = text.lower()

    punctuation = [".", ",", "!", "?", ":", ";", "(", ")", '"', "'"]
    for p in punctuation:
        text = text.replace(p, " ")

    words = text.split()

    unique_words = []
    for w in words:
        if w not in unique_words:
            unique_words.append(w)
    
    return unique_words


def compute_theme_score(words: list, word_probabilities: dict, files_per_theme: dict, theme: str, global_vocabulary: list) -> float:
    """Computes a numerical score of a file for a given theme based on word occurrences
    Parameters
    ----------
    words: list of unique words extracted from the file to be classified (list)
    word_probabilities: dictionary containing, for each theme, the probabilities P(word | theme)
    computed during training (dict)

    files_per_theme: dictionary indicating, for each theme, the number of learning files available (dict)
    theme: the theme for which we want to compute how well the file matches it, that is,
           the probability that the file belongs to this theme (str)

    global_vocabulary: list of all words encountered in all learning files, across all themes (list)

    Returns
    ----------
    score: numerical measure indicating how well the file matches the given theme;
    the higher the score, the more the file is considered to belong to this theme (float)
    """

    nb_themes = len(files_per_theme)
    if nb_themes == 0:
        return low_score
        
    p_theme = 1 / nb_themes
    score = math.log(p_theme)

    words_in_file_dict = {}
    for w in words:
        words_in_file_dict[w] = True
    
    for w in global_vocabulary:

        if w in word_probabilities[theme]:
            p_word_given_theme = word_probabilities[theme][w]
        else:
            total_files = files_per_theme[theme]
            p_word_given_theme = 1.0 / (total_files + 1)
        
        if w in words_in_file_dict:
            log_prob = math.log(p_word_given_theme) 
            score = score + log_prob
            
        else:
            p_not_word_given_theme = 1.0 - p_word_given_theme
            
            if p_not_word_given_theme == 0:
                log_prob = low_score
            else:
                log_prob = math.log(p_not_word_given_theme)
            
            score = score + log_prob

    return score


def classify_file(file_path: str, word_probabilities: dict, files_per_theme: dict, global_vocabulary: list):
    """Determines the theme that best matches a file using the naive bayes classifier

    Parameters
    ----------
    file_path: path to the text file to be classified (str)
    word_probabilities: dictionary of probabilities P(word | theme) computed from the learning files (dict)
    files_per_theme: dictionary of the number of files per theme used for learning (dict)
    global_vocabulary: list of all words encountered in all learning files (list)

    Returns
    ----------
    best_theme: the theme judged to be the most suitable for the file (str)
    """

    words = extract_words_from_file(file_path)

    best_theme = None
    best_score = None

    for theme in word_probabilities:
        score = compute_theme_score(words, word_probabilities, files_per_theme, theme, global_vocabulary)
        if best_score is None:
            best_score = score
            best_theme = theme

        elif score > best_score:
            best_score = score
            best_theme = theme

    return best_theme

def smart_sort_files(path: str):
    """Applies the complete classification process:
    builds the learning base from the 'sorted' folder.
    computes the conditional probabilities.
    classifies each file from the 'unsorted' folder into the 'sorted' subfolder corresponding to the predicted theme.

    Parameters
    ----------
        path: path to the root folder containing the 'sorted' and 'unsorted' subfolders (str)
    Returns
    ----------
        None
    """

    path_sorted = path + "/sorted"
    path_unsorted = path + "/unsorted"

    if not os.path.isdir(path_sorted):
        print("Error: 'sorted' folder not found")
        return 

    if not os.path.isdir(path_unsorted):
        print("Error: 'unsorted' folder not found")
        return 

    theme_word_counts, files_per_theme = build_learning_base(path_sorted)

    if not files_per_theme:
        print("No themes found in the 'sorted' folder. Classification canceled.")
        return 

    global_vocabulary = []
    for theme in theme_word_counts:
        for word in theme_word_counts[theme]:
            if word not in global_vocabulary:
                global_vocabulary.append(word)

    word_probabilities = compute_word_probabilities(theme_word_counts, files_per_theme)
    
    if not global_vocabulary:
        print("The global vocabulary is empty. Classification canceled.")
        return

    files = os.listdir(path_unsorted)

    count = 0

    for filename in files:
        file_path = path_unsorted + "/" + filename

        if os.path.isfile(file_path):

            theme = classify_file(file_path, word_probabilities, files_per_theme, global_vocabulary)

            if theme is not None:

                destination_folder = path_sorted + "/" + theme
                destination_path = destination_folder + "/" + filename

                if not os.path.isdir(destination_folder):
                    os.mkdir(destination_folder)

                os.replace(file_path, destination_path)
                print("%s has been classified into %s" % (filename, theme))
                count = count + 1
            
            else:
                print("The file %s could not be classified (no theme found)." % filename)


    print("Total number of files classified: %d" % count)


def check_accuracy(path: str):
    """Checks the sorting accuracy by comparing the final theme of files in the 'sorted' folder
    with the correct theme indicated in the 'labels.txt' file.

    Parameters
    ----------
        path: path to the root folder containing the 'sorted' folder and the 'labels.txt' file (str)
    Returns
    ----------
        None
    """

    path_labels = path + "/labels.txt"
    path_sorted = path + "/sorted"

    if not os.path.isfile(path_labels):
        print("Error: labels.txt file not found for verification.")
        return
    
    if not os.path.isdir(path_sorted):
        print("Error: 'sorted' folder not found.")
        return

    true_labels = {}
    
    f = open(path_labels, 'r') 
    
    for line in f:
        line_clean = line.strip()          
        parts = line_clean.split()       
        
        if len(parts) == 2:
            filename = parts[0]
            true_theme = parts[1]
            true_labels[filename] = true_theme
            
    f.close() 
    
    
    if not true_labels:
        print("The labels.txt file is empty or incorrectly formatted. Verification canceled.")
        return

    print("------------------------------------------------------------------")
    print("--- Sorting Accuracy Check ---")

    correctly_sorted = 0
    total_checked = 0
    
    all_themes_dirs = []
    
    for d in os.listdir(path_sorted):
        dir_path = path_sorted + "/" + d
        if os.path.isdir(dir_path):
            all_themes_dirs.append(d)


    for filename in true_labels:       
        true_theme = true_labels[filename]  
        
        file_found = False
        
        for predicted_theme_dir in all_themes_dirs:
          
            if not file_found: 
                
                current_file_path = path_sorted + "/" + predicted_theme_dir + "/" + filename
                if os.path.isfile(current_file_path):
                    file_found = True
                    total_checked = total_checked + 1
                    
                    if predicted_theme_dir == true_theme:
                        correctly_sorted = correctly_sorted + 1
            
    if total_checked > 0:
        accuracy = (correctly_sorted / total_checked) * 100
        print("Number of files checked: %d" % total_checked)
        print("Number of correctly sorted files: %d" % correctly_sorted)
        print("Accuracy: %.2f%%" % accuracy)

    else:
        print("No files with a valid label could be verified.")
    print("------------------------------------------------------------------")


smart_sort_files("C:/Users/Maximilien/max/Ecole/Unamur/Introduction à la programmation/projet_de_groupe_3_Q1B1_G9/projet_de_groupe_3_Q1B1_G9/archive_2")

check_accuracy("C:/Users/Maximilien/max/Ecole/Unamur/Introduction à la programmation/projet_de_groupe_3_Q1B1_G9/projet_de_groupe_3_Q1B1_G9/archive_2")
