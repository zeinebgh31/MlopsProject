import os
import sys
import pandas as pd
from fastapi import FastAPI, Query

# 1. CORRECTION PRIORITAIRE : On modifie le PATH avant tout import local
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 2. Maintenant on peut importer le moteur de recherche
try:
    from rechercheHybride import hybrid_search
except ImportError:
    # Sécurité supplémentaire pour certains environnements
    from src.rechercheHybride import hybrid_search

# 3. Initialisation de l'API
app = FastAPI(
    title="EquipSearch API", 
    description="Moteur de recherche hybride (Sémantique + Lexical) pour catalogue industriel"
)

# 4. Chargement sécurisé du catalogue
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE_PATH = os.path.join(BASE_DIR, 'data', 'catalogue_nettoye_10k.csv')

if not os.path.exists(CATALOGUE_PATH):
    raise FileNotFoundError(f"Le catalogue est introuvable à l'adresse : {CATALOGUE_PATH}")

df = pd.read_csv(CATALOGUE_PATH)

@app.get("/")
def home():
    return {
        "message": "API EquipSearch opérationnelle", 
        "version": "1.0",
        "status": "success"
    }

@app.get("/search")
def search(q: str = Query(..., min_length=3, description="La requête de recherche"), k: int = 5):
    # Appel de la fonction de recherche
    results = hybrid_search(q, k=k)
    
    response_data = []
    for idx, score in results:
        # On vérifie que l'index existe dans le dataframe pour éviter les erreurs
        if idx < len(df):
            row = df.iloc[idx]
            # On formate le score pour qu'il soit lisible (0 à 100%)
            confidence = f"{min(99.9, score * 100):.2f}%" if score < 1 else f"{min(99.9, score):.2f}%"
            
            response_data.append({
                "designation": row['designation'],
                "score_confiance": confidence,
                "index_original": int(idx)
            })
    
    return {
        "query": q,
        "total_results": len(response_data),
        "results": response_data
    }