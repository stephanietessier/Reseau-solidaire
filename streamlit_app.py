import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from src.matching import charger_donnees, calculer_matches

st.set_page_config(page_title="Réseau de solidarité locale IA", page_icon="🤝", layout="wide")

st.title("🤝 Réseau de solidarité locale IA")
st.markdown("Une démonstration éthique qui relie les besoins urgents aux ressources locales disponibles.")

besoins, ressources = charger_donnees(ROOT / "data/besoins.csv", ROOT / "data/ressources.csv")

categorie = st.sidebar.selectbox("Filtrer par catégorie", ["Toutes"] + sorted(besoins["categorie"].unique().tolist()))
top_n = st.sidebar.slider("Nombre de ressources recommandées par besoin", 1, 5, 3)

if categorie != "Toutes":
    besoins_filtrees = besoins[besoins["categorie"] == categorie]
else:
    besoins_filtrees = besoins

matches = calculer_matches(besoins_filtrees, ressources, top_n=top_n)

col1, col2, col3 = st.columns(3)
col1.metric("Besoins actifs", len(besoins_filtrees))
col2.metric("Ressources disponibles", len(ressources[ressources["disponibilite"] == "oui"]))
col3.metric("Matches générés", len(matches))

st.subheader("Meilleures connexions")
st.dataframe(matches, use_container_width=True)

st.subheader("Carte des besoins")
fig_besoins = px.scatter_mapbox(
    besoins_filtrees,
    lat="latitude",
    lon="longitude",
    hover_name="nom",
    hover_data=["categorie", "urgence", "description"],
    zoom=10,
    height=420,
)
fig_besoins.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_besoins, use_container_width=True)

st.subheader("Créer un nouveau besoin")
with st.form("nouveau_besoin"):
    nom = st.text_input("Nom ou organisme")
    quartier = st.text_input("Quartier", "Montréal")
    categorie_new = st.selectbox("Catégorie", ["nourriture", "logement", "entraide"])
    description = st.text_area("Description du besoin")
    urgence = st.slider("Urgence", 1, 5, 3)
    submitted = st.form_submit_button("Trouver des ressources")

if submitted:
    nouveau = pd.DataFrame([{
        "id_besoin": "NOUVEAU",
        "nom": nom or "Nouveau besoin",
        "quartier": quartier,
        "latitude": 45.5017,
        "longitude": -73.5673,
        "categorie": categorie_new,
        "description": description,
        "urgence": urgence,
        "beneficiaires": 1,
        "contact": "à compléter",
    }])
    recommandations = calculer_matches(nouveau, ressources, top_n=5)
    st.success("Ressources recommandées")
    st.dataframe(recommandations, use_container_width=True)

st.caption("Prototype éducatif. Ne pas utiliser sans validation humaine pour des situations critiques.")
