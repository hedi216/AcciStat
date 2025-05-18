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
def map_departements():
    return {
        "75": "Paris", "13": "Bouches-du-Rhône", "69": "Rhône",
        "33": "Gironde", "59": "Nord", "31": "Haute-Garonne",
        "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne",
        "77": "Seine-et-Marne", "78": "Yvelines", "91": "Essonne",
        "95": "Val-d'Oise", "38": "Isère", "34": "Hérault",
        "44": "Loire-Atlantique", "35": "Ille-et-Vilaine", "67": "Bas-Rhin"
    }

df = load_data()
dep_map = map_departements()

df = df[df['dep'].notna() & df['mois'].notna()]
df['dep'] = df['dep'].astype(str).str.zfill(2)
df['departement_nom'] = df['dep'].map(dep_map)

# Sidebar filtres
st.sidebar.header("🔎 Filtres")
annees = sorted(df['annee'].dropna().unique())
departements = sorted(dep_map.items(), key=lambda x: x[1])

annee_selectionnee = st.sidebar.selectbox("Année", annees, index=len(annees) - 1)
dep_selectionne = st.sidebar.selectbox("Département", [f"{code} - {nom}" for code, nom in departements])
dep_code = dep_selectionne.split(" - ")[0]

# Filtrage
df_filtre = df[(df['annee'] == annee_selectionnee) & (df['dep'] == dep_code)]
st.success(f"{len(df_filtre):,} accidents affichés pour {dep_map[dep_code]} en {annee_selectionnee}")

# Affichage global
col1, col2, col3 = st.columns(3)
col1.metric("Total accidents", len(df_filtre))
col2.metric("Mois le plus accidentogène", int(df_filtre['mois'].mode()[0]))
col3.metric("% GPS connus", f"{100 * df_filtre['lat'].notna().mean():.1f}%")

# Répartition mensuelle
st.subheader("📆 Accidents par mois")
mois = df_filtre['mois'].value_counts().sort_index()
fig_mois = px.bar(x=mois.index, y=mois.values, labels={'x': 'Mois', 'y': 'Nb accidents'})
st.plotly_chart(fig_mois, use_container_width=True)

# Luminosité
st.subheader("💡 Conditions de luminosité")
labels_lum = {
    1: "Plein jour", 2: "Crépuscule / aube", 3: "Nuit sans éclairage",
    4: "Nuit avec éclairage non allumé", 5: "Nuit avec éclairage"
}
df_filtre['lum_label'] = df_filtre['lum'].map(labels_lum)
fig_lum = px.pie(df_filtre, names='lum_label', title="Accidents selon la luminosité")
st.plotly_chart(fig_lum, use_container_width=True)

# Conditions atmosphériques
st.subheader("🌧 Conditions météo")
labels_atm = {
    1: "Normale", 2: "Pluie légère", 3: "Pluie forte", 4: "Neige", 5: "Brouillard",
    6: "Vent fort", 7: "Temps éblouissant", 8: "Temps couvert", 9: "Autre"
}
df_filtre['atm_label'] = df_filtre['atm'].map(labels_atm)
fig_atm = px.histogram(df_filtre, x='atm_label', color='atm_label', title="Répartition par météo")
st.plotly_chart(fig_atm, use_container_width=True)

# Type de collision
st.subheader("🚗 Types de collision")
labels_col = {
    1: "Deux véhicules frontale",
    2: "Deux véhicules arrière",
    3: "Deux véhicules angle",
    4: "Trois véhicules et +",
    5: "Autre collision",
    6: "Sans collision",
    7: "Autre"
}
df_filtre['col_label'] = df_filtre['col'].map(labels_col)
fig_col = px.bar(df_filtre['col_label'].value_counts(), orientation='h', title="Distribution des types de collision")
st.plotly_chart(fig_col, use_container_width=True)
