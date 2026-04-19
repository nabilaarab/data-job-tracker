from pathlib import Path
import os

def load_key_words(filepath_keywords: str) -> list[str]:
    # Read the file of key words
    with open(filepath_keywords, "r", encoding="utf-8") as f:
        key_words = []
        for line in f:
            key_words.append(line.strip())
    
    return key_words

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()
    
def get_latest_file(
        path_folder:    str, 
        extension:      str = "*.xlsx"
    ):
    folder = Path(path_folder)
    
    # 1. Lister les fichiers correspondants
    files = list(folder.glob(extension))
    
    # 2. Vérifier si des fichiers existent pour éviter une erreur
    if not files:
        return None
        
    # 3. Trouver le fichier avec la date de modification (mtime) la plus grande
    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    
    return str(latest_file)
