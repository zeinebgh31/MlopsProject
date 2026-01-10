
# PROJET MLOPS : EQUIP-SEARCH API

## DESCRIPTION DU PROJET
Ce projet déploie un moteur de recherche Hybride haute performance pour un catalogue d'équipements industriels.

### Les technologies utilisées :
* **Backend :** FastAPI (Python 3.12)
* **Moteur Sémantique :** FAISS + Sentence-Transformers
* **Moteur Lexical :** BM25
* **Déploiement :** Docker

---

## 📊 PERFORMANCE (RECALL@1)
**Score de Recall@1 atteint : 88%**

Ce score garantit que dans **88% des cas**, l'équipement exact recherché est le premier résultat proposé.

---

## 📂 STRUCTURE DU RÉPERTOIRE
L'organisation respecte les standards de développement logiciel :

* `📂 src/` : Code source (API et Logique de recherche).
* `📂 data/` : Catalogue d'équipements (Base de connaissances).
* `📂 evaluation/` : Rapports de tests et calculs de métriques.
* `📄 Dockerfile` : Recette de l'image de déploiement.
* `📄 requirements.txt` : Liste des bibliothèques nécessaires.

---

## GUIDE DE LANCEMENT RAPIDE

### 1️⃣ Via Docker (Méthode recommandée)
Utilisez ces deux commandes pour lancer l'API instantanément :


# Construction de l'image
docker build -t equip-api .

# Lancement du container 

docker run -p 8000:8000 equip-api

### 2️⃣ Test de l'API
Une fois lancé, ouvrez votre navigateur à l'adresse suivante : 👉 http://localhost:8000/docs

⚙️ FONCTIONNEMENT TECHNIQUE
Le moteur de recherche utilise une fusion de scores :

Compréhension Contextuelle : Utilisation de all-MiniLM-L6-v2 pour capter l'intention de l'utilisateur.

Précision Technique : BM25 pour ne pas rater les références de modèles exactes.

Algorithme : Les résultats sont classés par une moyenne pondérée des deux approches.
