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
passwords = [generate_password(random.randint(6, 15)) for _ in range(10)]  # 1000 mots de passe aléatoires
df = pd.DataFrame(passwords, columns=['password'])
df['category'] = df['password'].apply(categorize_password)
df['hashed_password'] = df['password'].apply(hash_md5)  # Chiffrer en MD5

# Connexion à la base de données MySQL
try:
    # Connexion à la base de données MySQL
    connection = mysql.connector.connect(
        host='localhost',
        port='8889',           # Assurez-vous que ce port est correct
        database='password_db',  # Remplacez par le nom de votre base de données
        user='root',      # Nom d'utilisateur MySQL
        password='root'  # Mot de passe MySQL (vide par défaut dans MAMP)
    )

    if connection.is_connected():
        print("Connexion réussie à la base de données MySQL.")
        
        # Insérer les données dans la base de données
        cursor = connection.cursor()
        
        # Créer une table si elle n'existe pas déjà
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            original_password VARCHAR(255),
            hashed_password VARCHAR(255),
            category VARCHAR(50)
        );
        """)
        
        # Insérer les mots de passe et leurs catégories
        for index, row in df.iterrows():
            cursor.execute("""
            INSERT INTO passwords (original_password, hashed_password, category)
            VALUES (%s, %s, %s)
            """, (row['password'], row['hashed_password'], row['category']))
        
        # Commit les changements
        connection.commit()
        print("Les mots de passe ont été insérés dans la base de données.")

except Error as e:
    print(f"Erreur lors de la connexion à MySQL : {e}")

finally:
    # Vérifie si la connexion existe et est active
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connexion MySQL fermée.")

