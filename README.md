<div align="center">
  <a href="https://blent.ai">
    <img src="https://blent-static-media.s3.eu-west-3.amazonaws.com/images/logo/logo_blent_300x.png" alt="Logo Blent.ai" width="200" />
  </a>

  <h2 align="center">Étude et analyse des accidents corporels de la circulation routière</h2>

  <p align="center">
    Projet Data Engineering - <a href="https://blent.ai">Blent.ai</a>
    <br />
    <a href="https://blent.ai/app/projects" target="_blank"><strong>Explorer tous les projets »</strong></a>
</div>

<div align="center"><img src="https://cdn-icons-png.flaticon.com/512/1576/1576488.png" width="140" alt="Badge du projet" /></div>

## À propos du projet

Ce projet a pour but de vous initier aux techniques d'analyse de données et de visualisation avec Python. Vous utiliserez des bibliothèques telles que **Pandas, Matplotlib, Seaborn**, et **Plotly** pour explorer et visualiser les données des accidents corporels de la circulation routière 2022 de France. Ensuite, vous intégrerez vos visualisations dans une application interactive Streamlit et déploierez cette application sur Streamlit Cloud.

L'objectif final est de créer un tableau de bord interactif permettant de mieux comprendre les accidents corporels de la circulation routière et de faciliter la prise de décisions.

## Étapes du projet

- [ ] Explorer les datasets pour étudier les propriétés statistiques des variables
- [ ] Nettoyer et préparer les données pour l'analyse
- [ ] Créer des visualisations de données avec Matplotlib, Seaborn, et Plotly
- [ ] Intégrer les visualisations dans une application Streamlit
- [ ] Déployer l'application sur Streamlit Cloud

## Résultats attendus

Une fois le projet terminé, vous devriez avoir un tableau de bord interactif qui présente les données des accidents de manière claire et attrayante, en utilisant diverses visualisations.  

Le tableau de bord doit inclure deux pages, une pour analyser de manière globale les accidents de l'année 2022 avec des bar chart, séries temporelles, pie chart etc. et dans la deuxième page une carte avec tous les accidents avec la possibilités de filtrer sur des colonnes spécifiques comme le département où a eu lieu l'accident, les conditions atmosphériques, type de collision etc.

- **Tableau de bord**

![dashboard-1](https://i.postimg.cc/fWKPjjdf/image.png)

![dashboard-2](https://i.postimg.cc/GthqSVDJ/image.png)

- **Carte des accidents routiers**

![carte-sf](https://i.postimg.cc/KvWJJ98B/image.png)

![carte-af](https://i.postimg.cc/rpXgLKWp/image.png)

> Note: Ces graphiques et filtres sont juste à titre d'exemples, vous pouvez les adapter selon les besoins analytiques que vous jugez nécessaires.

## Structure du projet
Le dépôt Git contient les éléments suivants :

`notebooks/` : contient les Notebooks Jupyter du projet  
`streamlit/` : contient l'application Streamlit  
`data/` : contient les jeux de données  
`LICENSE.txt` : licence du projet  
`requirements.txt` : liste des dépendances Python   
`README.md` : fichier description du projet

## Premiers pas
Les instructions suivantes vous permettent d'exécuter le projet sur votre PC.

### Pré-requis
Le projet nécessite Python 3 d'installé sur le système.

### Installation

- Cloner le projet Git :

```bash
git clone https://github.com/Hamagistral/Projet-Data-Eng-Accidents.git
```

- Installer les dépendances du fichier requirements.txt dans un environnement virtuel.

Linux / MacOS

```bash
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

Windows

```bash
python -m venv venv/
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Démarrage
- Lancer un Notebook Jupyter pour explorer et analyser les données :

```bash
jupyter notebook notebooks/your_notebook.ipynb
```

- Pour lancer l'application Streamlit en local :

```bash
streamlit run app/app.py
```

- Déploiement

Pour déployer votre application sur Streamlit Cloud :

1. Connectez-vous à [Streamlit Cloud](https://streamlit.io/cloud).
2. Créez une nouvelle application en reliant votre dépôt GitHub.
C3. onfigurez les paramètres de déploiement et lancez votre application.