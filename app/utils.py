
def load_key_words(filepath_keywords: str) -> list[str]:
    # Read the file of key words
    with open(filepath_keywords, "r", encoding="utf-8") as f:
        key_words = []
        for line in f:
            key_words.append(line.strip())
    
    return key_words
