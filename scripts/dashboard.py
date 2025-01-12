import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configurer la page Streamlit
st.set_page_config(page_title="Dashboard Interactif - Pathologies EEG", layout="wide")

# Fonction pour générer l'interprétation
def generate_interpretation(filtered_df, disorder):
    """
    Génère une liste à puces d'interprétation basée sur les résultats filtrés.
    """
    if filtered_df.empty:
        return "Aucune donnée disponible pour cette pathologie."

    row = filtered_df.iloc[0]

    # Vérifier si les colonnes nécessaires existent
    required_columns = ['Band', 'Metric', 'Mean AUC (95% CI)', 'Mean Sensitivity (95% CI)', 'Mean Specificity (95% CI)', 'p-value']
    for col in required_columns:
        if col not in row:
            return f"La colonne '{col}' est manquante dans les données filtrées."

    # Créer une liste à puces
    interpretation_list = [
        f"**Bande et Métrique Utilisées** : La meilleure performance a été obtenue avec la bande **{row['Band']}** et la métrique **{row['Metric']}**. Les troubles obsessionnels compulsifs obtiennent de moins bonnes performances, ce qui pourrait s'expliquer par un déséquilibre des classes.",
        f"**AUC** : L'AUC observée est de **{row['Mean AUC (95% CI)']}**, indiquant une bonne capacité de discrimination du modèle.",
        f"**Sensibilité** : La sensibilité moyenne est de **{row['Mean Sensitivity (95% CI)']}**, suggérant que le modèle détecte efficacement les vrais positifs.",
        f"**Spécificité** : La spécificité moyenne est de **{row['Mean Specificity (95% CI)']}**, indiquant que le modèle identifie correctement les vrais négatifs.",
        f"**Significativité Statistique** : La p-value est de **{row['p-value']}**, confirmant que les performances du modèle sont statistiquement significatives et supérieures au hasard. Leur manque de variance peut s'expliquer par le faible nombre de permutations utilisées lors du test.",
        f"Ces résultats démontrent que le modèle est performant pour classifier **{disorder}** par rapport aux sujets sains."
    ]

    return "\n\n".join([f"- {item}" for item in interpretation_list])

# Charger les données
BASE_DIR = Path(__file__).parent
processed_data_path = BASE_DIR / "../data/processed/processed_data.csv"
final_results_path = BASE_DIR / "../dashboard/assets/final_results.csv"

# Vérifier l'existence des fichiers
if not processed_data_path.exists():
    st.error(f"Fichier introuvable : {processed_data_path}")
if not final_results_path.exists():
    st.error(f"Fichier introuvable : {final_results_path}")

# Charger les données si disponibles
if processed_data_path.exists() and final_results_path.exists():
    df = pd.read_csv(processed_data_path)
    df["main.disorder"] = df["main.disorder"].map(lambda x: x if x != "healthy control" else "Healthy Control")
    final_results_df = pd.read_csv(final_results_path)
    count_data = df.groupby(["main.disorder"]).size().reset_index(name="Count")

    # Interface utilisateur
    st.title("Dashboard Interactif - Pathologies EEG")

    # Introduction
    with st.expander("Introduction"):
        st.markdown("""
        - **Band et Metric** : Type de bande de fréquences EEG et la métrique associée (AB = PSD (Power Spectral Density) et COH = Cohérence).
        - **Mean AUC (95% CI)** : Aire sous la courbe ROC et son intervalle de confiance à 95 %.
        - **Mean Sensitivity & Mean Specificity (95% CI)** : Sensibilité et spécificité moyennes avec leurs IC à 95 %.
        - **p-value** : Reflète la significativité statistique (test de permutation) pour déterminer si la performance est au-dessus du hasard.
        - **Healthy Control** : Groupe témoin pour comparer avec les différentes pathologies.
        """)

    # Sélection de la pathologie
    disorders = df["main.disorder"].unique()
    disorders = [d for d in disorders if d != "Healthy Control"]
    selected_disorder = st.selectbox("Sélectionnez une pathologie :", disorders, index=0)

    # Mise en page en deux colonnes
    #col1, col2 = st.columns([2, 3])

    # Mise en page en deux colonnes
col1, col2 = st.columns([3, 2]) 

# Mise en page en deux colonnes : tableau et barplot
col1, col2 = st.columns([3, 2])  # Ajuste les proportions des colonnes

# Colonne 1 : Tableau des résultats filtrés
with col1:
    st.subheader("Tableau des résultats filtrés")
    filtered_df = final_results_df[final_results_df["main.disorder"] == selected_disorder]
    # Afficher le tableau sans l'index
    st.table(filtered_df)


# Colonne 2 : Barplot des effectifs
with col2:
    st.subheader("Barplot des effectifs")
    filtered_counts = count_data[count_data["main.disorder"].isin(["Healthy Control", selected_disorder])]

    fig = px.bar(
        filtered_counts,
        x="main.disorder",
        y="Count",
        text="Count",
        title=f"Effectifs - Healthy Control vs {selected_disorder}",
        labels={"main.disorder": "Catégorie", "Count": "Effectif"},
        color="main.disorder",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Ajustements pour un barplot compact
    fig.update_layout(
        title_x=0.5,
        height=350,  # Réduire la hauteur
        margin=dict(l=10, r=10, t=40, b=20),
        plot_bgcolor="#2c2c2c",  # Fond sombre
        paper_bgcolor="#2c2c2c"  # Fond sombre
    )

    # Améliorations des barres et des textes
    fig.update_traces(
        width=0.5,                   # Réduire la largeur des barres
        textposition="outside",      # Texte à l'extérieur
        textfont=dict(size=12, color="white"),  # Texte blanc
        marker=dict(line=dict(width=1, color='white'))  # Bordures blanches
    )

    st.plotly_chart(fig, use_container_width=True)

# Section Interprétation en dessous
st.subheader("Interprétation des Résultats")
interpretation = generate_interpretation(filtered_df, selected_disorder)
st.markdown(interpretation, unsafe_allow_html=True)