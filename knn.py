import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix

# Étape 1 : Charger les données depuis le fichier RockYou.txt
file_path = 'mdp.txt'  # Remplace par le chemin correct de ton fichier
with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
    passwords = file.readlines()

# Nettoyage des données : suppression des espaces et des lignes vides
passwords = [password.strip() for password in passwords if password.strip()]

# Conversion en DataFrame pour faciliter la manipulation
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

# Appliquer la fonction de catégorisation aux mots de passe
df['category'] = df['password'].apply(categorize_password)

# Étape 2 : Préparer les données pour l'entraînement du modèle
# Vectoriser les mots de passe
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['password']).toarray()
y = df['category']

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Étape 3 : Entraîner le modèle KNN
knn = KNeighborsClassifier(n_neighbors = 9)  # Choisir k = 5
knn.fit(X_train, y_train)

# Étape 4 : Évaluer le modèle
y_pred = knn.predict(X_test)

# Afficher le rapport de classification
print(classification_report(y_test, y_pred))

# Afficher la matrice de confusion
print(confusion_matrix(y_test, y_pred))


# 937832bf2aaf916fcc2418432a60dfe8
# 937832bf2aaf916fcc2418432a60dfe8