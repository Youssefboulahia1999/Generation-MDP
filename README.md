# 🔐 **Analyse et Classification des Mots de Passe avec KNN et MySQL**

## 📚 **Description du Projet**  
Ce projet vise à générer, catégoriser, chiffrer et analyser des mots de passe à l'aide de Python, MySQL et d'un modèle de Machine Learning (K-Nearest Neighbors).

### 📝 **Fonctionnalités**  
- **Génération de mots de passe aléatoires** (faible, moyen, fort).  
- **Catégorisation des mots de passe** via des règles définies.  
- **Chiffrement MD5** pour sécuriser les mots de passe.  
- **Stockage dans une base MySQL** pour une gestion centralisée.  
- **Classification avec KNN** pour prédire la force d'un mot de passe.  
- **Évaluation du modèle** avec un rapport de classification et une matrice de confusion.
- 
## 🛠️ **Technologies Utilisées**  
- **Python**  
- **Pandas**  
- **Scikit-learn**  
- **MySQL**  
- **Hashlib**  
- **Regex**

- ## 🚀 **Installation**  

1. **Clone le dépôt :**  
   ```bash
   git clone https://github.com/ton-repo.git
   cd ton-repo
   ```

2. **Installe les dépendances :**  
   ```bash
   pip install pandas scikit-learn mysql-connector-python
   ```

3. **Configure la connexion MySQL dans le script :**  
   ```python
   host='localhost'
   port='8888'
   database='password_db'
   user='root'
   password=''
   ```

4. **Exécute le script :**  
   ```bash
   python main.py

   ## 📊 **Sorties Attentues**  
- **Liste des mots de passe générés et chiffrés.**  
- **Stockage des mots de passe dans une base MySQL.**  
- **Rapport de classification KNN.**  
- **Matrice de confusion.**
