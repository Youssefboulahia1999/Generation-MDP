import spacy
import random

# Charger le modèle de langue anglaise
nlp = spacy.load("en_core_web_sm")

def is_common_word(password):
    doc = nlp(password)
    for token in doc:
        if token.is_stop or token.lemma_ == password.lower():
            return True
    return False

def contains_common_patterns(password):
    # Vous pouvez ajouter ici une logique pour vérifier des motifs communs
    # Par exemple, vérifier si le mot de passe contient "123", "password", etc.
    common_patterns = ["123", "password", "qwerty", "abc"]
    for pattern in common_patterns:
        if pattern in password.lower():
            return True
    return False

def generate_password(length):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_chars = "!@#$%^&*()-_=+"
    all_chars = lowercase + uppercase + digits + special_chars
    while True:
        password = "".join(random.choice(all_chars) for _ in range(length))
        if not contains_common_patterns(password) and not is_common_word(password):
            return password

# Exemple d’utilisation
print(generate_password(28))
