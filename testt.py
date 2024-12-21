import pandas as pd
import re

# Étape 1 : Charger les données depuis le fichier RockYou.txt
file_path = 'rockyou.txt'  # Remplace par le chemin correct de ton fichier
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

# Sauvegarde des données dans un fichier CSV
df.to_csv('passwords_cleaned.csv', index=False)

# Afficher la distribution des catégories
print(df['category'].value_counts())

# Afficher quelques exemples de mots de passe avec leur catégorie
print(df.head())
