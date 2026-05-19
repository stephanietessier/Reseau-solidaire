import math
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def haversine_km(lat1, lon1, lat2, lon2):
    """Calcule la distance approximative entre deux coordonnées GPS."""
    r = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def charger_donnees(besoins_path="data/besoins.csv", ressources_path="data/ressources.csv"):
    besoins = pd.read_csv(besoins_path)
    ressources = pd.read_csv(ressources_path)
    return besoins, ressources


def calculer_matches(besoins, ressources, top_n=3):
    """
    Associe chaque besoin aux meilleures ressources.
    Score = similarité texte + catégorie + proximité + urgence + capacité.
    """
    besoins = besoins.copy()
    ressources = ressources.copy()

    besoins["texte"] = besoins["categorie"].fillna("") + " " + besoins["description"].fillna("")
    ressources["texte"] = ressources["categorie"].fillna("") + " " + ressources["description"].fillna("")

    vectorizer = TfidfVectorizer(stop_words="english")
    corpus = pd.concat([besoins["texte"], ressources["texte"]], ignore_index=True)
    vecteurs = vectorizer.fit_transform(corpus)
    besoin_vecs = vecteurs[: len(besoins)]
    ressource_vecs = vecteurs[len(besoins) :]
    sim_matrix = cosine_similarity(besoin_vecs, ressource_vecs)

    resultats = []
    for i, besoin in besoins.iterrows():
        candidats = []
        for j, ressource in ressources.iterrows():
            if str(ressource.get("disponibilite", "oui")).lower() != "oui":
                continue

            distance = haversine_km(
                besoin["latitude"], besoin["longitude"],
                ressource["latitude"], ressource["longitude"]
            )
            score_texte = float(sim_matrix[i, j])
            score_categorie = 1.0 if besoin["categorie"] == ressource["categorie"] else 0.0
            score_distance = max(0, 1 - distance / 15)  # 1 proche, 0 au-delà de 15 km
            score_urgence = besoin["urgence"] / 5
            score_capacite = min(1, ressource["capacite"] / max(1, besoin["beneficiaires"]))

            score_total = (
                0.35 * score_texte
                + 0.25 * score_categorie
                + 0.20 * score_distance
                + 0.10 * score_urgence
                + 0.10 * score_capacite
            )

            candidats.append({
                "id_besoin": besoin["id_besoin"],
                "nom": besoin["nom"],
                "categorie_besoin": besoin["categorie"],
                "description_besoin": besoin["description"],
                "urgence": besoin["urgence"],
                "id_ressource": ressource["id_ressource"],
                "organisation": ressource["organisation"],
                "categorie_ressource": ressource["categorie"],
                "description_ressource": ressource["description"],
                "distance_km": round(distance, 2),
                "score": round(score_total * 100, 1),
                "contact_ressource": ressource["contact"],
            })

        meilleurs = sorted(candidats, key=lambda x: x["score"], reverse=True)[:top_n]
        resultats.extend(meilleurs)

    return pd.DataFrame(resultats)


if __name__ == "__main__":
    besoins, ressources = charger_donnees()
    matches = calculer_matches(besoins, ressources)
    print(matches[["id_besoin", "nom", "organisation", "distance_km", "score"]])
