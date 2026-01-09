import json
import re
import csv

def clean_title(text):
    """
    Fonction de nettoyage (Normalisation) selon les besoins du projet :
    - Enlève les tags de langue comme '@en'
    - Enlève les caractères spéciaux (| , : " )
    - Met tout en minuscule
    - Supprime les espaces inutiles
    """
    if not text:
        return ""
    
    # 1. Supprimer les tags de langue (ex: "@en")
    text = re.sub(r'@\w+', '', text)
    
    # 2. Supprimer les caractères spéciaux spécifiques et la ponctuation bruyante
    # On garde les tirets car ils sont souvent importants dans les modèles techniques
    text = re.sub(r'[|":]', ' ', text)
    
    # 3. Mise en minuscule
    text = text.lower()
    
    # 4. Nettoyage des espaces multiples
    text = " ".join(text.split())
    
    return text

# Configuration des fichiers
input_file_path = "C:/Users/msi/Downloads/offers_corpus_english_v2_non_norm.json/translatedOffers_englishV2"  # Remplacez par le nom exact de votre fichier
output_file_path = "catalogue_nettoye_10k.csv"
max_lines = 10000

print(f"Début de l'extraction de {max_lines} lignes...")

results = []

try:
    with open(input_file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            
            # Charger la ligne JSON
            try:
                data = json.loads(line)
                raw_title = data.get('title', '')
                
                # Nettoyer le titre
                cleaned = clean_title(raw_title)
                
                if cleaned:
                    results.append(cleaned)
            except json.JSONDecodeError:
                continue

    # Sauvegarder dans un fichier CSV léger pour le groupe
    with open(output_file_path, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["designation"]) # En-tête
        for row in results:
            writer.writerow([row])

    print(f"Terminé ! Fichier sauvegardé sous : {output_file_path}")
    print(f"Nombre de titres uniques extraits : {len(set(results))}")

except FileNotFoundError:
    print("Erreur : Le fichier source est introuvable. Vérifiez le nom du fichier .jsonl")
