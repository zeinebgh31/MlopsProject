import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import re

# --- INITIALISATION ---
df = pd.read_csv('data/catalogue_nettoye_10k.csv')
documents = df['designation'].astype(str).tolist()

# 1. Préparation pour BM25 (Tokenisation simple)
tokenized_corpus = [doc.split(" ") for doc in documents]
bm25 = BM25Okapi(tokenized_corpus)

# 2. Préparation pour FAISS (Chargement de l'index existant)
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("models/index.faiss")

# --- FONCTION DE CALIBRATION ---
def calibrate_score(distance, method="semantic"):
    """Transforme une distance ou un score brut en pourcentage 0-100%"""
    if method == "semantic":
        # Pour FAISS L2, une distance de 0 est parfaite. 
        # On utilise une fonction pour mapper [0, 1.5] vers [100, 0]
        score = max(0, 100 - (distance * 50))
    else:
        # Pour BM25, le score dépend de la longueur de la requête.
        # On normalise de façon simplifiée pour le projet.
        score = min(100, distance * 5) 
    return score

# --- FONCTION HYBRIDE ---
def hybrid_search(query, k=5):
    query_clean = query.lower()
    
    # A. Recherche Sémantique (FAISS)
    query_vector = model.encode([query_clean]).astype('float32')
    distances, indices = index.search(query_vector, k)
    
    # B. Recherche Lexicale (BM25)
    query_tokens = query_clean.split(" ")
    bm25_scores = bm25.get_scores(query_tokens)
    top_bm25_indices = np.argsort(bm25_scores)[::-1][:k]
    
    # C. Fusion et Scoring (Hybrid)
    combined_results = {}
    
    # Ajouter résultats FAISS
    for i in range(len(indices[0])):
        idx = indices[0][i]
        score_sem = calibrate_score(distances[0][i], "semantic")
        combined_results[idx] = score_sem * 0.7 # Poids de 70% pour le sémantique
        
    # Ajouter/Fusionner résultats BM25
    for idx in top_bm25_indices:
        score_lex = calibrate_score(bm25_scores[idx], "lexical")
        if idx in combined_results:
            combined_results[idx] += score_lex * 0.3 # Poids de 30% pour le lexical
        else:
            combined_results[idx] = score_lex * 0.3
            
    # Trier par score final
    sorted_ids = sorted(combined_results.items(), key=lambda x: x[1], reverse=True)[:k]
    
    return sorted_ids

# --- TEST ---
query_test = "krowne 15-812l faucet"
results = hybrid_search(query_test)

print(f"Résultats Hybrides pour : {query_test}")
for idx, score in results:
    print(f"- {documents[idx]} | Confidence: {score:.2f}%")