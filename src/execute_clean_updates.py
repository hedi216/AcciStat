from cleaning import load_and_clean_data
import os
import datetime
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration
RAW_DATA_DIR = "../data"
DB_URL = "mysql+pymysql://root:@localhost/accidents"

def get_latest_year_in_db():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT MAX(annee) FROM caracteristiques"))
            max_year = result.scalar()
            return max_year if max_year else 0
    except Exception as e:
        print(f"❌ Erreur lors de la connexion à la base : {e}")
        return 0

def get_available_years():
    files = os.listdir(RAW_DATA_DIR)
    years = set()
    for f in files:
        for prefix in ['caracteristiques', 'caracteristiques_']:
            if f.startswith(prefix) and f.endswith(".csv"):
                parts = f.replace(".csv", "").split("_")[-1].split("-")
                try:
                    year = int(parts[-1])
                    years.add(year)
                except:
                    continue
    return sorted(years)

def main():
    print("\n🚀 Lancement du processus automatique de mise à jour...")
    latest_year = get_latest_year_in_db()
    available_years = get_available_years()

    print(f"🔍 Année la plus récente en base : {latest_year}")
    print(f"📂 Années disponibles dans les fichiers : {available_years}")

    for year in available_years:
        if year > latest_year:
            load_and_clean_data(year)

if __name__ == "__main__":
    main()
