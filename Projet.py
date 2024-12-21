import pandas as pd
import re
import random
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
import spacy

# Charger le modèle de langue anglaise
nlp = spacy.load("en_core_web_sm")

# Fonction pour vérifier si un mot de passe est un mot courant
def is_common_word(password):
    doc = nlp(password)
    for token in doc:
        if token.is_stop or token.lemma_ == password.lower():
            return True
    return False

# Fonction pour vérifier les motifs communs dans un mot de passe
def contains_common_patterns(password):
    common_patterns = ["123", "password", "qwerty", "abc"]
    for pattern in common_patterns:
        if pattern in password.lower():
            return True
    return False

# Fonction pour générer des mots de passe
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

# Générer un ensemble de mots de passe
passwords = [generate_password(random.randint(6, 15)) for _ in range(1000)]  # 1000 mots de passe aléatoires

# Création du DataFrame
df = pd.DataFrame(passwords, columns=['password'])

# Suppression des doublons
df = df.drop_duplicates()

# Normalisation : mots de passe en minuscules
df['password'] = df['password'].str.lower()

# Fonction pour catégoriser les mots de passe
def categorize_password(password):
    if len(password) < 6:
        return 'faible'
    elif 6 <= len(password) <= 10:
        if re.search(r'[0-9]', password) or re.search(r'[^a-zA-Z0-9]', password):
            return 'moyen'
        else:
            return 'faible'
    else:
        if (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and re.search(r'[^a-zA-Z0-9]', password)):
            return 'fort'
        else:
            return 'moyen'

# Appliquer la fonction de catégorisation
df['category'] = df['password'].apply(categorize_password)

# Écrire les mots de passe et leurs catégories dans un fichier texte
output_file = 'passwords_and_categories.txt'
with open(output_file, 'w') as f:
    for index, row in df.iterrows():
        f.write(f"{row['password']}\t{row['category']}\n")

print(f"Les mots de passe et leurs catégories ont été enregistrés dans {output_file}.")

# Étape 2 : Préparer les données pour l'entraînement
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['password']).toarray()
y = df['category']

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Étape 3 : Entraîner le modèle KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Étape 4 : Évaluer le modèle
y_pred = knn.predict(X_test)

# Afficher le rapport de classification
print(classification_report(y_test, y_pred))

# Afficher la matrice de confusion
print(confusion_matrix(y_test, y_pred))
