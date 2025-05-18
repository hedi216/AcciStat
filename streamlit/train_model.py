import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import traceback

print("📅 Chargement des données par échantillon")

engine = create_engine("mysql+pymysql://root:@localhost/accidents")
all_data = []
resume_par_annee = {}

for year in range(2005, 2024):
    print(f"🔹 Lecture {year}...")
    try:
        carac = pd.read_sql(f"SELECT * FROM caracteristiques WHERE annee = {year} LIMIT 20000", con=engine)
        lieux = pd.read_sql("SELECT * FROM lieux", con=engine)
        usagers = pd.read_sql("SELECT * FROM usagers", con=engine)
        vehicules = pd.read_sql("SELECT * FROM vehicules", con=engine)

        # Nettoyage
        for df in [carac, lieux, usagers, vehicules]:
            df.columns = df.columns.str.strip()
            df['Num_Acc'] = df['Num_Acc'].astype(str)

            # Injecte annee depuis Num_Acc si manquante ou vide
            if 'annee' not in df.columns or df['annee'].isnull().all():
                df['annee'] = df['Num_Acc'].str[:4].astype(int)

        # Supprimer 'annee' sauf dans carac
        for df in [lieux, usagers, vehicules]:
            if 'annee' in df.columns:
                df.drop(columns=['annee'], inplace=True)

        # Renommage dynamique
        if 'id_vehicule' not in usagers.columns and 'num_veh' in usagers.columns:
            usagers.rename(columns={'num_veh': 'id_vehicule'}, inplace=True)
        if 'id_vehicule' not in vehicules.columns and 'num_veh' in vehicules.columns:
            vehicules.rename(columns={'num_veh': 'id_vehicule'}, inplace=True)

        df = carac.merge(lieux, on="Num_Acc", how="left")

        if 'id_vehicule' in vehicules.columns:
            if 'id_vehicule' in df.columns:
                df = df.merge(vehicules, on=["Num_Acc", "id_vehicule"], how="left")
            else:
                df = df.merge(vehicules, on="Num_Acc", how="left")
        else:
            df = df.merge(vehicules, on="Num_Acc", how="left")

        if 'id_vehicule' in usagers.columns:
            if 'id_vehicule' in df.columns:
                df = df.merge(usagers, on=["Num_Acc", "id_vehicule"], how="left")
            else:
                df = df.merge(usagers, on="Num_Acc", how="left")
        else:
            df = df.merge(usagers, on="Num_Acc", how="left")

        colonnes_utiles = ['grav', 'lum', 'atm', 'agg', 'int', 'col',
                           'catv', 'manv', 'prof', 'plan', 'surf', 'sexe', 'an_nais']

        valides = df[colonnes_utiles].dropna()
        resume_par_annee[year] = valides.shape[0]

        if valides.shape[0] > 0:
            all_data.append(valides)
        else:
            print(f"⏭️ Année {year} ignorée (seulement 0 lignes valides)")

    except Exception as e:
        print(f"⚠️ Erreur pour {year} : {e}")
        traceback.print_exc()

# Récapitulatif
print("\n🔹 Résumé des lignes valides par année :")
for y, n in resume_par_annee.items():
    print(f"  - {y} : {n} lignes valides")

# Entraînement
if all_data:
    data = pd.concat(all_data, ignore_index=True)
    print(f"\n✅ Données finales pour entraînement : {data.shape}")

    X = data.drop(columns=['grav'])
    y = data['grav']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n📊 Rapport de classification :")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "model_grav.pkl")
    print("✅ Modèle sauvegardé dans model_grav.pkl")
else:
    print("\n❌ Aucune donnée suffisante pour entraîner un modèle.")
