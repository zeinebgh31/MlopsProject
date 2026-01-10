import pandas as pd
import numpy as np
import faiss
import time
from sentence_transformers import SentenceTransformer


print("Chargement du catalogue...")
df = pd.read_csv('catalogue_nettoye_10k.csv')
sentences = df['designation'].astype(str).tolist()


print("Chargement du modèle NLP...")
model = SentenceTransformer('all-MiniLM-L6-v2')


print(f"Génération des vecteurs pour {len(sentences)} lignes... (cela peut prendre un moment)")
start_time = time.time()
embeddings = model.encode(sentences, show_progress_bar=True)
print(f"Vecteurs générés en {time.time() - start_time:.2f} secondes.")


dimension = embeddings.shape[1] 
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))


faiss.write_index(index, "index.faiss")
print("Index FAISS sauvegardé avec succès !")

query = "heavy duty industrial faucet"
print(f"\nTest de recherche pour : '{query}'")
query_vector = model.encode([query])
D, I = index.search(np.array(query_vector).astype('float32'), k=5)

print("\nTop 5 des correspondances :")
for i in range(len(I[0])):
    idx = I[0][i]
    print(f"- {sentences[idx]} (Distance: {D[0][i]:.4f})")
