import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Prédiction de la gravite", layout="centered")
st.title("🔮 Prédiction de la gravité d'un accident")

# Chargement du modèle
@st.cache_resource
def load_model():
    return joblib.load("model_grav.pkl")

model = load_model()

# Dictionnaires de correspondance lisibles
lum_options = {
    1: "Plein jour",
    2: "Crépuscule ou aube",
    3: "Nuit sans éclairage",
    4: "Nuit avec éclairage non allumé",
    5: "Nuit avec éclairage allumé"
}
atm_options = {
    1: "Normale",
    2: "Pluie légère",
    3: "Pluie forte",
    4: "Neige - grêle",
    5: "Brouillard - fumée",
    6: "Vent fort",
    7: "Temps éblouissant",
    8: "Temps couvert",
    9: "Autre"
}
agg_options = {1: "Hors agglomération", 2: "En agglomération"}
int_options = {
    1: "Hors intersection",
    2: "Intersection en X",
    3: "Intersection en T",
    4: "Intersection en Y",
    5: "Intersection à plus de 4 branches",
    6: "Giratoire"
}
col_options = {
    1: "Deux véhicules - frontale",
    2: "Deux véhicules - par l’arrière",
    3: "Deux véhicules - par le côté",
    4: "Trois véhicules et plus - en chaîne",
    5: "Trois véhicules et plus - collisions multiples",
    6: "Autre collision",
    7: "Sans collision"
}
sexe_options = {1: "Homme", 2: "Femme"}

catv_options = {
    1: "Vélo",
    2: "Cyclomoteur <50cm3",
    7: "Voiture",
    10: "Poids lourd",
    13: "Bus",
    21: "Tramway",
    30: "Engin spécial",
    37: "Trottinette électrique",
    38: "Gyropode",
    39: "Hoverboard",
    40: "Autre",
}

manv_options = {
    1: "Sans changement de direction",
    2: "Même sens - changement de file",
    3: "Même sens - dépassement",
    4: "Même sens - tourne à gauche",
    5: "Même sens - tourne à droite",
    6: "Sens opposé - tourne à gauche",
    7: "Sens opposé - tourne à droite",
    8: "Franchit terre-plein central",
    9: "Change de direction et tourne à gauche",
    10: "Change de direction et tourne à droite",
    11: "Marche arrière",
    12: "Manoeuvre de stationnement",
    13: "Ouverture de porte"
}

prof_options = {
    1: "Plat",
    2: "Pente",
    3: "Sommet de côte",
    4: "Bas de côte",
    5: "Inconnu"
}
plan_options = {
    1: "Partie rectiligne",
    2: "En courbe à gauche",
    3: "En courbe à droite",
    4: "Changement de direction"
}
surf_options = {
    1: "Normale",
    2: "Mouillée",
    3: "Flaques",
    4: "Inondée",
    5: "Enneigée",
    6: "Verglacée",
    7: "Autre"
}

# Formulaire utilisateur
with st.form("prediction_form"):
    st.write("### Renseignez les caractéristiques de l'accident")

    col1, col2 = st.columns(2)
    with col1:
        lum = st.selectbox("Conditions de lumière (lum)", list(lum_options.keys()), format_func=lambda x: lum_options[x])
        atm = st.selectbox("Conditions atmosphériques (atm)", list(atm_options.keys()), format_func=lambda x: atm_options[x])
        agg = st.selectbox("Zone (agg)", list(agg_options.keys()), format_func=lambda x: agg_options[x])
        int_ = st.selectbox("Type d'intersection (int)", list(int_options.keys()), format_func=lambda x: int_options[x])
        col = st.selectbox("Type de collision (col)", list(col_options.keys()), format_func=lambda x: col_options[x])
    with col2:
        catv = st.selectbox("Type de véhicule (catv)", list(catv_options.keys()), format_func=lambda x: catv_options[x])
        manv = st.selectbox("Manœuvre (manv)", list(manv_options.keys()), format_func=lambda x: manv_options[x])
        prof = st.selectbox("Profil de la route (prof)", list(prof_options.keys()), format_func=lambda x: prof_options[x])
        plan = st.selectbox("Plan de la route (plan)", list(plan_options.keys()), format_func=lambda x: plan_options[x])
        surf = st.selectbox("État de la chaussée (surf)", list(surf_options.keys()), format_func=lambda x: surf_options[x])

    sexe = st.radio("Sexe du conducteur", list(sexe_options.keys()), format_func=lambda x: sexe_options[x], horizontal=True)
    an_nais = st.slider("Année de naissance du conducteur", 1920, 2020, 1990)

    submitted = st.form_submit_button("Prédire la gravité")

if submitted:
    # Données sous forme de DataFrame
    features = pd.DataFrame.from_dict([{
        "lum": lum,
        "atm": atm,
        "agg": agg,
        "int": int_,
        "col": col,
        "catv": catv,
        "manv": manv,
        "prof": prof,
        "plan": plan,
        "surf": surf,
        "sexe": sexe,
        "an_nais": an_nais,
    }])

    # Prédiction
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    labels = {
        1: "Indemne",
        2: "Tué",
        3: "Blessé hospitalisé",
        4: "Blessé léger"
    }

    st.markdown("---")
    st.subheader("🔬 Résultat de la prédiction :")
    st.success(f"Gravité prédite : **{labels.get(prediction, 'Inconnu')} ({int(prediction)})**")

    st.write("### Probabilités associées :")
    for i, p in enumerate(proba, start=1):
        st.write(f"{labels.get(i, i)} : {p:.2%}")
