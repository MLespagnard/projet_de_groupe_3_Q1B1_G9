BAN_WORDS = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "for",
    "is", "are", "was", "were", "be", "been", "this", "that",
    "with", "as", "by", "it", "from"
}

def read_clean_words(filename):
    
    f = open(filename, 'r')
    text = f.read()
    f.close()

    text = text.lower()

    # Remove weird Character
    for ch in ".,;:!?()[]{}<>\"'@#/\\=+-*":
        text = text.replace(ch, " ")
    
    words = text.split()

    clean_words = []
    for word in words:
        if word and word not in BAN_WORDS:
            clean_words.append(word)
    
    return clean_words



read_clean_words("sorted/comp.graphics/37261")