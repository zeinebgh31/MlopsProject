import pandas as pd
import numpy as np
import faiss
import time
from sentence_transformers import SentenceTransformer

# 1. Chargement des données
print("Chargement du catalogue...")
df = pd.read_csv('catalogue_nettoye_10k.csv')
sentences = df['designation'].astype(str).tolist()

# 2. Choix du modèle (Le "cerveau" de votre IA)
# 'all-MiniLM-L6-v2' est le meilleur compromis vitesse/précision pour l'anglais
print("Chargement du modèle NLP...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Génération des Embeddings (Transformation en vecteurs)
print(f"Génération des vecteurs pour {len(sentences)} lignes... (cela peut prendre un moment)")
start_time = time.time()
embeddings = model.encode(sentences, show_progress_bar=True)
print(f"Vecteurs générés en {time.time() - start_time:.2f} secondes.")

# 4. Création de l'index FAISS
# On utilise IndexFlatL2 pour une recherche exacte par distance Euclidienne
dimension = embeddings.shape[1] # Pour ce modèle, c'est 384
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

# 5. Sauvegarde de l'index et des données (Indispensable pour Docker plus tard)
faiss.write_index(index, "index.faiss")
print("Index FAISS sauvegardé avec succès !")

# --- TEST RAPIDE ---
query = "heavy duty industrial faucet"
print(f"\nTest de recherche pour : '{query}'")
query_vector = model.encode([query])
D, I = index.search(np.array(query_vector).astype('float32'), k=5)

print("\nTop 5 des correspondances :")
for i in range(len(I[0])):
    idx = I[0][i]
    print(f"- {sentences[idx]} (Distance: {D[0][i]:.4f})")