import pandas as pd

# 1. Charger le catalogue que vous venez de créer
df = pd.read_csv('catalogue_nettoye_10k.csv')

# 2. Prendre 50 lignes au hasard
test_samples = df.sample(n=50, random_state=42) # random_state pour que ce soit reproductible

# 3. Créer une colonne vide pour vos requêtes inventées
test_samples['user_query'] = ""

# 4. Sauvegarder pour le travail manuel
test_samples.to_csv('creation_test_set.csv', index=False)

print("Fichier 'creation_test_set.csv'  ")
