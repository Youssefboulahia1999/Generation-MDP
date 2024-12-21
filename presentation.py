import pandas as pd
import re
import random
import hashlib
import mysql.connector
from mysql.connector import Error
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

# Connexion à la base de données MySQL et récupération des mots de passe
try:
    connection = mysql.connector.connect(
        host='localhost',
        port='8889',
        database='password_db',  # Nom de votre base de données
        user='root',
        password='root'
    )

    if connection.is_connected():
        print("Connexion réussie à la base de données MySQL.")
        
        # Récupérer les données depuis MySQL
        query = "SELECT original_password, category FROM passwords;"
        df = pd.read_sql(query, connection)
        print("Données récupérées depuis la base de données MySQL.")
        
except Error as e:
    print(f"Erreur lors de la connexion à MySQL : {e}")
    df = pd.DataFrame(columns=['original_password', 'category'])  # Données vides en cas d'erreur

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connexion MySQL fermée.")

# Étape 1 : Prétraitement des données
if not df.empty:
    df['hashed_password'] = df['original_password'].apply(hash_md5)  # Ajouter une colonne MD5

    # Préparation des données pour le modèle KNN
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['original_password']).toarray()  # Transformation en vecteurs numériques
    y = df['category']

    # Séparation en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Étape 2 : Entraîner le modèle KNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    # Étape 3 : Évaluation du modèle
    y_pred = knn.predict(X_test)
    print("\nRapport de classification :")
    print(classification_report(y_test, y_pred))
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    # Étape 4 : Génération de nouveaux mots de passe et prédiction de leur catégorie
    new_passwords = [generate_password(random.randint(6, 15)) for _ in range(10)]
    new_df = pd.DataFrame(new_passwords, columns=['original_password'])

    # Vectorisation des nouveaux mots de passe
    X_new = vectorizer.transform(new_df['original_password']).toarray()
    new_df['category'] = knn.predict(X_new)  # Prédire les catégories
    new_df['hashed_password'] = new_df['original_password'].apply(hash_md5)

    print("\nNouveaux mots de passe générés avec prédiction des catégories :")
    print(new_df)

    # Étape 5 : Insérer les nouveaux mots de passe dans la base de données
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='8889',
            database='password_db',
            user='root',
            password='root'
        )

        if connection.is_connected():
            print("Connexion à la base de données pour insertion des nouveaux mots de passe.")
            cursor = connection.cursor()

            # Insérer chaque mot de passe généré
            for index, row in new_df.iterrows():
                cursor.execute("""
                INSERT INTO passwords (original_password, hashed_password, category)
                VALUES (%s, %s, %s)
                """, (row['original_password'], row['hashed_password'], row['category']))

            connection.commit()
            print("Les nouveaux mots de passe ont été insérés dans la base de données.")

    except Error as e:
        print(f"Erreur lors de l'insertion dans MySQL : {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée.")

else:
    print("Aucune donnée n'a été récupérée pour l'entraînement.")
