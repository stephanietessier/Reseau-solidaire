# 🤝 Réseau de solidarité locale IA

Prototype progressiste d'intelligence artificielle pour connecter en temps réel des besoins locaux — logement, nourriture, entraide — avec des ressources communautaires disponibles.

Ce projet est conçu pour être :

- prêt à déposer sur GitHub ;
- prêt à exécuter dans Google Colab ;
- utilisable comme démonstrateur Streamlit ;
- simple à adapter pour une ville, une association ou un collectif.

> ⚠️ Important : ce prototype utilise des données imaginées. Il ne remplace jamais le jugement humain, le travail social, les services d'urgence ou les organismes publics.

---

## Fonctionnalités

- Chargement de besoins communautaires depuis un CSV.
- Chargement de ressources disponibles depuis un CSV.
- Matching IA avec :
  - similarité textuelle TF-IDF ;
  - catégorie du besoin ;
  - distance géographique ;
  - urgence ;
  - capacité de la ressource.
- Tableau de recommandations.
- Carte interactive avec Streamlit + Plotly.
- Formulaire pour tester un nouveau besoin.

---

## Structure du projet

```text
reseau_solidarite_ia/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── besoins.csv
│   └── ressources.csv
├── notebooks/
│   └── Colab_Demo_Reseau_Solidarite_IA.ipynb
├── src/
│   └── matching.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Lancer en local

```bash
git clone https://github.com/VOTRE-NOM/reseau_solidarite_ia.git
cd reseau_solidarite_ia
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## Utiliser dans Google Colab

1. Ouvrir `notebooks/Colab_Demo_Reseau_Solidarite_IA.ipynb`.
2. Exécuter les cellules dans l'ordre.
3. Modifier les données dans les DataFrames ou importer vos CSV.

---

## Comment fonctionne le score ?

Le score final combine :

```text
35 % similarité texte
25 % même catégorie
20 % proximité géographique
10 % niveau d'urgence
10 % capacité de la ressource
```

Cette logique est volontairement transparente pour éviter une IA opaque dans un contexte social sensible.

---

## Idées d'amélioration

- Ajouter une base de données SQLite ou PostgreSQL.
- Ajouter une authentification pour les organismes.
- Ajouter un module SMS ou courriel.
- Ajouter une validation humaine obligatoire avant mise en relation.
- Ajouter une journalisation éthique des décisions.
- Ajouter des règles de protection des données personnelles.

---

## Licence suggérée

MIT pour le code. Pour des données réelles, utiliser une licence et une politique de confidentialité adaptées.
