import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import load_table

st.set_page_config(page_title="Dashboard Accidents", layout="wide")
st.title("📊 Analyse des accidents de la route")

@st.cache_data
def load_data():
    return load_table("caracteristiques")

@st.cache_data
def load_usagers():
    return load_table("usagers")

@st.cache_data
def map_departements():
    return {
        "75": "Paris", "13": "Bouches-du-Rhône", "69": "Rhône",
        "33": "Gironde", "59": "Nord", "31": "Haute-Garonne",
        "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne",
        "77": "Seine-et-Marne", "78": "Yvelines", "91": "Essonne",
        "95": "Val-d'Oise", "38": "Isère", "34": "Hérault",
        "44": "Loire-Atlantique", "35": "Ille-et-Vilaine", "67": "Bas-Rhin"
    }

@st.cache_data
def map_lum():
    return {
        1: "Plein jour", 2: "Crépuscule / aube", 3: "Nuit sans éclairage",
        4: "Nuit sans éclairage public", 5: "Nuit avec éclairage public"
    }

@st.cache_data
def map_atm():
    return {
        1: "Normale", 2: "Pluie légère", 3: "Pluie forte", 4: "Neige", 5: "Brouillard",
        6: "Vent fort", 7: "Temps éblouissant", 8: "Temps couvert", 9: "Autre"
    }

# Chargement et préparation des données
df = load_data()
usagers = load_usagers()
dep_map = map_departements()
lum_map = map_lum()
atm_map = map_atm()

df = df[df['dep'].notna() & df['mois'].notna()]
df['dep'] = df['dep'].astype(str).str.zfill(2)
df['departement_nom'] = df['dep'].map(dep_map)
df['lum_label'] = df['lum'].map(lum_map)
df['atm_label'] = df['atm'].map(atm_map)
df['Num_Acc'] = df['Num_Acc'].astype(str)
usagers['Num_Acc'] = usagers['Num_Acc'].astype(str)

# 🧹 Filtres principaux
st.sidebar.header("🔎 Filtres principaux")
annees = sorted(df['annee'].dropna().unique())
departements = sorted(dep_map.items(), key=lambda x: x[1])

annee_selectionnee = st.sidebar.selectbox("Année", annees, index=len(annees) - 1)
dep_selectionne = st.sidebar.selectbox("Département", [f"{code} - {nom}" for code, nom in departements])
dep_code = dep_selectionne.split(" - ")[0]

# Filtres secondaires
st.sidebar.header("🎛️ Filtres secondaires")
lum_filter = st.sidebar.multiselect("Luminosité", list(lum_map.values()), default=list(lum_map.values()))
atm_filter = st.sidebar.multiselect("Conditions météo", list(atm_map.values()), default=list(atm_map.values()))

# 📄 Export CSV
st.sidebar.header("💾 Export")
if st.sidebar.button("Exporter CSV"):
    st.sidebar.download_button("Télécharger", df.to_csv(index=False), "accidents.csv", "text/csv")

# Filtrage des données
filtre = (
    (df['annee'] == annee_selectionnee) &
    (df['dep'] == dep_code) &
    (df['lum_label'].isin(lum_filter)) &
    (df['atm_label'].isin(atm_filter))
)
df_filtre = df[filtre]
st.success(f"{len(df_filtre):,} accidents affichés pour {dep_map[dep_code]} en {annee_selectionnee}")

# Jointure avec les usagers
df_fusion = pd.merge(df_filtre, usagers[['Num_Acc', 'sexe', 'an_nais']], on="Num_Acc", how="left")

# KPIs principaux
col1, col2, col3 = st.columns(3)
col1.metric("Total accidents", len(df_filtre))
col2.metric("Mois le plus accidentogène", int(df_filtre['mois'].mode()[0]))
col3.metric("% GPS connus", f"{100 * df_filtre['lat'].notna().mean():.1f}%")

# Visualisations
with st.expander("🗓️ Accidents par mois"):
    mois = df_filtre['mois'].value_counts().sort_index()
    fig_mois = px.bar(x=mois.index, y=mois.values, labels={'x': 'Mois', 'y': 'Nb accidents'})
    st.plotly_chart(fig_mois, use_container_width=True)

with st.expander(" Accidents par jour du mois"):
    jours = df_filtre['jour'].value_counts().sort_index()
    fig_jour = px.bar(x=jours.index, y=jours.values, labels={'x': 'Jour', 'y': 'Accidents'})
    st.plotly_chart(fig_jour, use_container_width=True)

with st.expander("🔦 Répartition par luminosité"):
    fig_lum = px.pie(df_filtre, names='lum_label', title="Accidents selon la luminosité")
    st.plotly_chart(fig_lum, use_container_width=True)

with st.expander("🌧 Répartition par météo"):
    fig_atm = px.histogram(df_filtre, x='atm_label', color='atm_label', title="Conditions atmosphériques")
    st.plotly_chart(fig_atm, use_container_width=True)

with st.expander("🚗 Types de collision"):
    labels_col = {
        1: "Deux véhicules frontale", 2: "Deux véhicules arrière", 3: "Deux véhicules angle",
        4: "Trois véhicules et +", 5: "Autre collision", 6: "Sans collision", 7: "Autre"
    }
    if 'col' in df_filtre.columns:
        df_filtre['col_label'] = df_filtre['col'].map(labels_col)
        fig_col = px.bar(df_filtre['col_label'].value_counts(), orientation='h', title="Types de collision")
        st.plotly_chart(fig_col, use_container_width=True)

with st.expander("🚻 Répartition par sexe", expanded=False):
    if 'sexe' in df_fusion.columns and df_fusion['sexe'].notna().sum() > 0:
        df_valid = df_fusion[df_fusion['sexe'].notna()]
        df_sample = df_valid.sample(n=1000, random_state=42) if len(df_valid) > 1000 else df_valid
        labels_sexe = {1: "Homme", 2: "Femme"}
        df_sample['sexe_label'] = df_sample['sexe'].map(labels_sexe)
        sexe_counts = df_sample['sexe_label'].value_counts()
        fig = px.pie(values=sexe_counts.values, names=sexe_counts.index, title="Répartition des accidents par sexe")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de sexe disponible pour ces filtres.")

with st.expander("📊 Répartition par tranche d'âge", expanded=False):
    if 'an_nais' in df_fusion.columns and df_fusion['an_nais'].notna().sum() > 0:
        df_valid = df_fusion[df_fusion['an_nais'].notna()].copy()
        df_valid['age'] = annee_selectionnee - df_valid['an_nais']
        df_valid = df_valid[df_valid['age'].between(10, 100)]

        if not df_valid.empty:
            df_sample = df_valid.sample(n=1000, random_state=42) if len(df_valid) > 1000 else df_valid
            df_sample['tranche_age'] = pd.cut(df_sample['age'],
                bins=[10, 20, 30, 40, 50, 60, 70, 100],
                labels=["10-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71+"])
            fig = px.histogram(df_sample, x='tranche_age', title="Répartition par tranche d'âge")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de naissance exploitable pour ce filtre.")
    else:
        st.info("Aucune donnée de naissance disponible pour ces filtres.")