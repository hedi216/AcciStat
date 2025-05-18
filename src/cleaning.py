import pandas as pd
import os
import shutil
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def load_and_clean_data(year: int, raw_data_path: str = "../data", cleaned_data_path: str = "data/cleaned", archive_path: str = "../archive") -> pd.DataFrame:
    try:
        engine = create_engine("mysql+pymysql://root:@localhost/accidents")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM caracteristiques WHERE annee = :year"), {"year": year})
            if result.scalar() > 0:
                print(f"⏭️ Année {year} ignorée (déjà présente en base).")
                return pd.DataFrame()
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification des données en base : {e}")
        return pd.DataFrame()

    print(f"\n📅 Traitement des données pour l'année {year}")

    if year == 2009:
        sep = '\t'
    elif year <= 2018:
        sep = ','
    else:
        sep = ';'

    def file_name(base):
        return f"{base}_{year}.csv" if year <= 2016 else f"{base}-{year}.csv"

    try:
        df_carac = pd.read_csv(f"{raw_data_path}/{file_name('caracteristiques')}", sep=sep, low_memory=False, encoding='ISO-8859-1')

        if year == 2009:
            lieux_cols = ["Num_Acc", "catr", "voie", "v1", "v2", "circ", "nbv", "pr", "pr1", "vosp", "prof", "plan", "lartpc", "larrout", "surf", "infra", "situ", "env1"]
            usagers_cols = ["Num_Acc", "place", "catu", "grav", "sexe", "trajet", "secu", "locp", "actp", "etatp", "an_nais", "num_veh"]
            vehicules_cols = ["Num_Acc", "senc", "catv", "occutc", "obs", "obsm", "choc", "manv", "num_veh"]

            df_lieux = pd.read_csv(f"{raw_data_path}/{file_name('lieux')}", sep='\t', names=lieux_cols, skiprows=1, encoding='ISO-8859-1')
            df_usagers = pd.read_csv(f"{raw_data_path}/{file_name('usagers')}", sep='\t', names=usagers_cols, skiprows=1, encoding='ISO-8859-1')
            df_vehicules = pd.read_csv(f"{raw_data_path}/{file_name('vehicules')}", sep='\t', names=vehicules_cols, skiprows=1, encoding='ISO-8859-1')
        else:
            df_lieux = pd.read_csv(f"{raw_data_path}/{file_name('lieux')}", sep=sep, encoding='ISO-8859-1')
            df_usagers = pd.read_csv(f"{raw_data_path}/{file_name('usagers')}", sep=sep, encoding='ISO-8859-1')
            df_vehicules = pd.read_csv(f"{raw_data_path}/{file_name('vehicules')}", sep=sep, encoding='ISO-8859-1')
    except FileNotFoundError as e:
        print(f"❌ Fichier manquant : {e}")
        return pd.DataFrame()
    except pd.errors.ParserError as e:
        print(f"❌ Erreur de parsing : {e}")
        return pd.DataFrame()

    if 'num_veh' in df_usagers.columns and 'id_vehicule' not in df_usagers.columns:
        df_usagers.rename(columns={'num_veh': 'id_vehicule'}, inplace=True)
    if 'num_veh' in df_vehicules.columns and 'id_vehicule' not in df_vehicules.columns:
        df_vehicules.rename(columns={'num_veh': 'id_vehicule'}, inplace=True)

    for df in [df_carac, df_lieux, df_usagers, df_vehicules]:
        df.columns = df.columns.str.strip()
        df['annee'] = year
        if 'Num_Acc' in df.columns:
            df['Num_Acc'] = df['Num_Acc'].astype(str)

    for df in [df_carac, df_lieux]:
        for col in ['lat', 'long', 'latit', 'longit']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

    try:
        df = df_carac.merge(df_lieux, on="Num_Acc", how="left")
        df = df.merge(df_vehicules, on=["Num_Acc", "id_vehicule"], how="left") if "id_vehicule" in df_vehicules.columns else df.merge(df_vehicules, on="Num_Acc", how="left")
        df = df.merge(df_usagers, on=["Num_Acc", "id_vehicule"], how="left") if "id_vehicule" in df_usagers.columns else df.merge(df_usagers, on="Num_Acc", how="left")
    except KeyError as e:
        print(f"❌ Erreur de fusion : {e}")
        return pd.DataFrame()

    os.makedirs(cleaned_data_path, exist_ok=True)
    output_file = f"{cleaned_data_path}/cleaned-{year}.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Données nettoyées enregistrées dans : {output_file}")

    try:
        df_carac.to_sql('caracteristiques', con=engine, if_exists='append', index=False)
        df_lieux.to_sql('lieux', con=engine, if_exists='append', index=False)
        df_usagers.to_sql('usagers', con=engine, if_exists='append', index=False)
        df_vehicules.to_sql('vehicules', con=engine, if_exists='append', index=False)
        print(f"✅ Données insérées dans MySQL pour {year}")
    except SQLAlchemyError as e:
        print(f"❌ Erreur MySQL : {e}")

    # 📦 Déplacement du fichier dans le dossier archive
    os.makedirs(archive_path, exist_ok=True)
    archive_file = os.path.join(archive_path, os.path.basename(output_file))
    try:
        shutil.move(output_file, archive_file)
        print(f"📁 Fichier déplacé vers : {archive_file}")
    except Exception as e:
        print(f"⚠️ Erreur lors du déplacement du fichier vers l'archive : {e}")

    return df
