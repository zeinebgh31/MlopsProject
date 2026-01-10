import pandas as pd


df = pd.read_csv('catalogue_nettoye_10k.csv')


test_samples = df.sample(n=50, random_state=42) 


test_samples['user_query'] = ""


test_samples.to_csv('creation_test_set.csv', index=False)

print("Fichier 'creation_test_set.csv'  ")
