import os

def build_learning_base(path_sorted):
    """
    Construit la base d’apprentissage à partir des fichiers d’un dossier "sorted".

    Le dossier "sorted" contient plusieurs sous-dossiers, chacun représentant un thème.
    Chaque sous-dossier contient plusieurs fichiers texte appartenant à ce thème.
    La fonction analyse ces fichiers afin de déterminer :
        - quels mots apparaissent dans chaque thème,
        - dans combien de fichiers du thème chaque mot apparaît.

    Pour chaque thème :
         tous les fichiers sont lus,
         les mots sont extraits (mise en minuscules, suppression de quelques ponctuations),
         on construit une liste des mots uniques présents dans CE fichier,
         chaque mot unique augmente son compteur : nombre de fichiers dans lesquels il apparaît.

    Paramètres
    ----------
    path_sorted : str
        Chemin vers le dossier "sorted" contenant un sous-dossier par thème.

    Returns
    -------
    theme_word_counts : dict
        Dictionnaire où :
             chaque clé est un thème (str),
             chaque valeur est un dictionnaire {mot : nombre de fichiers contenant ce mot dans ce thème}.

    files_per_theme : dict
        Dictionnaire où :
             chaque clé est un thème (str),
             chaque valeur est le nombre total de fichiers du thème.

    Remarques
    ---------
     Seuls les fichiers réguliers (pas les dossiers) sont lus.
     Aucun fichier n’est modifié.
     La fonction ignore les dossiers inexistants et retourne des dictionnaires vides dans ce cas.
    """

    theme_word_counts = {}
    files_per_theme = {}

    if not os.path.isdir(path_sorted):
        print("Erreur : dossier introuvable :", path_sorted)
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

                    # lecture du fichier
                    f = open(file_path, "r")
                    text = f.read()
                    f.close()
                    # passer en minuscules
                    text = text.lower()

                    # retirer quelques ponctuations
                    punctuation = [".", ",", "!", "?", ":", ";", "(", ")", '"', "'"]
                    for p in punctuation:
                        text = text.replace(p, " ")

                    words = text.split()

                    # créer la liste des mots uniques
                    unique_words = []
                    for w in words:
                        if w not in unique_words:
                            unique_words.append(w)

                    # ajouter à word_index
                    for w in unique_words:
                        if w not in theme_word_counts[theme]:
                            theme_word_counts[theme][w] = 1
                        else:
                            theme_word_counts[theme][w] = theme_word_counts[theme][w] + 1

    return theme_word_counts, files_per_theme

def compute_word_probabilities(theme_word_counts, files_per_theme):
    """
    Calcule les probabilités conditionnelles P(mot | thème) pour chaque mot
    et pour chaque thème, en utilisant la base d’apprentissage construite
    à partir du dossier "sorted".

    Pour chaque thème :
        - on connaît le nombre total de fichiers du thème,
        - on connaît, pour chaque mot, le nombre de fichiers du thème
          dans lesquels ce mot apparaît.

    La probabilité P(word | theme) est calculée selon la formule :
        (count(word, theme) + 1) / (files_per_theme[theme] + 1)

    Le "+1" (lissage additif) permet :
        - d'éviter d'obtenir une probabilité nulle si un mot n’apparaît
          dans aucun fichier du thème,
        - de pouvoir multiplier les probabilités sans annuler le produit.

    Paramètres
    ----------
    theme_word_counts : dict
        Dictionnaire où :
            - chaque clé est un thème (str),
            - chaque valeur est un dictionnaire {mot : nombre de fichiers contenant ce mot}.

    files_per_theme : dict
        Dictionnaire où :
            - chaque clé est un thème (str),
            - chaque valeur est le nombre total de fichiers du thème.

    Returns
    -------
    word_probabilities : dict
        Dictionnaire où :
            - chaque clé est un thème (str),
            - chaque valeur est un dictionnaire
              {mot : probabilité conditionnelle P(word | theme)}.

    Remarques
    ---------
    - Tous les mots de chaque thème reçoivent une probabilité.
    - Les mots absents d’un thème ne sont pas ajoutés ici.
      (Ils seront traités dans les fonctions suivantes au moment du test.)
    """
    word_probabilities = {}

    for theme in theme_word_counts:
        word_probabilities[theme] = {}
        total_files = files_per_theme[theme]

        for word in theme_word_counts[theme]:
            count = theme_word_counts[theme][word]

            # P(word | theme) = (count + 1) / (total_files + 1)
            probability = (count + 1) / (total_files + 1)

            word_probabilities[theme][word] = probability

    return word_probabilities
