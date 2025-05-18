import os
import datetime
import requests
from pathlib import Path
from scraper import get_csv_links_for_year
from cleaning import load_and_clean_data

def download_file(url: str, output_path: str):
    r = requests.get(url)
    r.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(r.content)

def download_latest_year_data(data_dir="data") -> int:
    current_year = datetime.datetime.now().year
    target_year = current_year - 1  # Exemple : en 2025 → on télécharge les fichiers 2024
    Path(data_dir).mkdir(exist_ok=True)

    links = get_csv_links_for_year(target_year)

    available_files = []
    for key, url in links.items():
        if url:
            filename = f"{key}-{target_year}.csv"
            path = os.path.join(data_dir, filename)
            try:
                print(f"⬇️ Téléchargement de : {filename}")
                download_file(url, path)
                available_files.append(key)
            except Exception as e:
                print(f"⚠️ Erreur pendant le téléchargement de {filename} : {e}")
        else:
            print(f"⚠️ Fichier {key}-{target_year}.csv non trouvé, il sera ignoré.")

    if not available_files:
        print("❌ Aucun fichier disponible pour cette année.")
        return None

    return target_year

def update_all():
    year = download_latest_year_data()
    if year is None:
        print("⛔ Mise à jour annulée, aucun fichier à traiter.")
        return

    try:
        df_cleaned = load_and_clean_data(year)
        Path("data/cleaned").mkdir(parents=True, exist_ok=True)
        output_path = f"data/cleaned/accidents_cleaned_{year}.csv"
        df_cleaned.to_csv(output_path, index=False)
        print(f"✅ Données nettoyées sauvegardées dans : {output_path}")
    except Exception as e:
        print(f"❌ Erreur pendant le nettoyage des données : {e}")

if __name__ == "__main__":
    update_all()
