import pandas as pd
import numpy as np
import time
import os
import sys

# Ajouter le dossier racine au chemin pour importer src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.rechercheHybride import hybrid_search

def evaluate():
    print("🚀 Lancement de l'évaluation du modèle...")
    
    # 1. Chargement des fichiers
    try:
        test_df = pd.read_csv('data/creation_test_set_long_queries.csv')
        cat_df = pd.read_csv('data/catalogue_nettoye_10k.csv')
        catalogue = cat_df['designation'].astype(str).tolist()
    except FileNotFoundError as e:
        print(f"❌ Erreur : Fichier introuvable. {e}")
        return

    total_queries = len(test_df)
    recalls_at_1 = 0
    recalls_at_5 = 0
    reciprocal_ranks = []
    latencies = []

    print(f"Analyse de {total_queries} requêtes en cours...")

    # 2. Boucle de test
    for index, row in test_df.iterrows():
        vrai_produit = str(row['designation']).strip()
        requete = str(row['user_query']).strip()
        
        # Mesure de la latence
        start_time = time.time()
        # On récupère le top 5
        results = hybrid_search(requete, k=5)
        latencies.append(time.time() - start_time)
        
        # Extraire les noms des produits trouvés par l'IA
        # On suppose que hybrid_search renvoie une liste de tuples (index, score)
        produits_trouves = [catalogue[idx] for idx, score in results]

        # Calcul des métriques
        if vrai_produit in produits_trouves:
            rank = produits_trouves.index(vrai_produit) + 1
            # Recall @ 5
            recalls_at_5 += 1
            # Recall @ 1
            if rank == 1:
                recalls_at_1 += 1
            # Reciprocal Rank pour le MRR
            reciprocal_ranks.append(1 / rank)
        else:
            reciprocal_ranks.append(0)

    # 3. Calcul des moyennes
    m_recall_1 = (recalls_at_1 / total_queries) * 100
    m_recall_5 = (recalls_at_5 / total_queries) * 100
    m_mrr = np.mean(reciprocal_ranks)
    m_latency = np.mean(latencies) * 1000 # Conversion en ms

    # 4. Affichage des résultats
    print("\n" + "="*40)
    print("       RÉSULTATS DE L'ÉVALUATION")
    print("="*40)
    print(f"✅ Recall @ 1 : {m_recall_1:.2f} %")
    print(f"✅ Recall @ 5 : {m_recall_5:.2f} %")
    print(f"✅ MRR        : {m_mrr:.4f}")
    print(f"⏱️ Latence moy: {m_latency:.2f} ms")
    print("="*40)

    # Sauvegarde dans un fichier CSV pour le rapport
    metrics_df = pd.DataFrame({
        'Metric': ['Recall@1', 'Recall@5', 'MRR', 'Latency_ms'],
        'Value': [m_recall_1, m_recall_5, m_mrr, m_latency]
    })
    os.makedirs('evaluation', exist_ok=True)
    metrics_df.to_csv('evaluation/metrics_results.csv', index=False)
    print("💾 Résultats sauvegardés dans 'evaluation/metrics_results.csv'")

if __name__ == "__main__":
    evaluate()