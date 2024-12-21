import pandas as pd
import re
import random
import hashlib
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix

# Fonction pour chiffrer un mot de passe en MD5
def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

# Fonction pour générer des mots de passe
def generate_password(length):
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_chars = "!@#$%^&*()-_=+"
    all_chars = lowercase + uppercase + digits + special_chars
    return "".join(random.choice(all_chars) for _ in range(length))

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

# Générer des mots de passe et leurs catégories
passwords = [generate_password(random.randint(6, 15)) for _ in range(1000)]  # 1000 mots de passe aléatoires
df = pd.DataFrame(passwords, columns=['password'])
df['category'] = df['password'].apply(categorize_password)
df['hashed_password'] = df['password'].apply(hash_md5)  # Chiffrer en MD5

# Connexion à la base de données MySQL
import mysql.connector
from mysql.connector import Error

try:
    # Connexion à la base de données MySQL
    connection = mysql.connector.connect(
        host='localhost',
        port='8888',
        database='password_db',  # Remplacez par votre nom de base de données
        user='root',      # Remplacez par votre nom d'utilisateur MySQL
        password=''  # Remplacez par votre mot de passe MySQL
    )

    if connection.is_connected():
        print("Connexion réussie à la base de données MySQL.")

    # Votre logique ici (par exemple, insertion de données)

except Error as e:
    print(f"Erreur lors de la connexion à MySQL : {e}")

finally:
    # Vérifie si la connexion existe et est active
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connexion MySQL fermée.")

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
