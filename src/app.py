import os
import sys
import pandas as pd
from fastapi import FastAPI, Query


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


try:
    from rechercheHybride import hybrid_search
except ImportError:
    
    from src.rechercheHybride import hybrid_search


app = FastAPI(
    title="EquipSearch API", 
    description="Moteur de recherche hybride (Sémantique + Lexical) pour catalogue industriel"
)


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
    
    results = hybrid_search(q, k=k)
    
    response_data = []
    for idx, score in results:
        
        if idx < len(df):
            row = df.iloc[idx]
            
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
