 Equip-Search API : Moteur de Recherche Hybride 
Ce projet propose une solution de recherche intelligente pour un catalogue d'équipements, combinant la puissance de la recherche sémantique (Dense Retrieval)
et de la recherche par mots-clés (BM25).
L'objectif est de fournir des résultats extrêmement précis même lorsque les termes de recherche ne correspondent pas exactement aux descriptions du catalogue.

 Performances 
 Grâce à l'approche hybride, nous avons atteint des performances de pointe sur notre jeu de test :
 Recall@1 : 88%
 Précision : Haute fidélité sur les termes techniques. 
 
Installation et Lancement 
Le projet est entièrement "dockerisé" pour garantir un déploiement rapide et sans erreurs de dépendances.
🐳 Avec Docker (Recommandé) 
Construire l'image :Bashdocker build -t equip-search-api .
Lancer le container :Bashdocker run -p 8000:8000 equip-search-api
Accéder à l'API :Rendez-vous sur http://localhost:8000/docs pour tester les endpoints via l'interface interactive Swagger.
🐍 Installation locale (sans Docker)
Installer les dépendances :Bashpip install -r requirements.txt
Lancer l'application :Bashpython -m uvicorn src.app:app --host 0.0.0.0 --port 8000

 Architecture du ProjetLe projet est organisé selon les standards MLOps pour séparer le code, les données et la configuration :
├── data/               # Catalogue d'équipements (CSV)
├── src/                # Code source de l'application
│   ├── app.py          # API FastAPI
│   └── rechercheHybride.py    # Moteur de recherche hybride (FAISS + BM25)
├── evaluation/         # Scripts et résultats des tests de performance
├── Dockerfile          # Configuration de l'image Docker
├── requirements.txt    # Dépendances Python
└── .dockerignore       # Optimisation du build Docker

 Méthodologie :
 Recherche HybrideLe moteur utilise une combinaison pondérée de deux scores pour classer les résultats :
 Dense Retrieval (FAISS) : Utilise le modèle all-MiniLM-L6-v2 pour comprendre le contexte sémantique.
 Sparse Retrieval (BM25) : Assure une correspondance parfaite sur les références techniques et les numéros de modèles
  Technologies utiliséesBackend :FastAPI (Python)
  Vector Database : FAISS (Facebook AI Similarity Search)
  NLP : Sentence-Transformers (Hugging Face)
  Conteneurisation : Docker
  Traitement de données : Pandas, Scikit-learn
