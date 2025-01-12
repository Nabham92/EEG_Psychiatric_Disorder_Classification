import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import numpy as np

# Charger les données principales
df = pd.read_csv(r"data\processed\processed_data.csv")
df["main.disorder"] = df["main.disorder"].map(lambda x: x if x != "healthy control" else "Healthy Control")

# Charger les résultats finaux (tableau agrégé)
final_results_df = pd.read_csv(r"dashboard\assets\final_results.csv")

# Compter les effectifs par catégorie
count_data = df.groupby(["main.disorder"]).size().reset_index(name="Count")

# Initialiser l'application Dash
app = dash.Dash(__name__)

# ----- FONCTION D'INTERPRÉTATION -----
def generate_interpretation(filtered_df, disorder):
    """
    Génère une liste à puces d'interprétation basée sur les résultats filtrés.
    """
    if filtered_df.empty:
        return html.P("Aucune donnée disponible pour cette pathologie.", style={"fontSize": "16px"})
    
    row = filtered_df.iloc[0]
    
    # Vérifier si les colonnes nécessaires existent
    required_columns = ['Band', 'Metric', 'Mean AUC (95% CI)', 'Mean Sensitivity (95% CI)', 'Mean Specificity (95% CI)', 'p-value']
    for col in required_columns:
        if col not in row:
            return html.P(f"La colonne '{col}' est manquante dans les données filtrées.", style={"fontSize": "16px"})
    
    # Créer une liste à puces
    interpretation_list = [
        html.Li(f"**Bande et Métrique Utilisées** : La meilleure performance a été obtenue avec la bande **{row['Band']}** et la métrique **{row['Metric']}**. Les troubles obsessionnels compulsifs obtiennent de moins bonnes performances, ce qui pourrait s'expliquer par un déséquilibre des classes."),
        html.Li(f"**AUC** : L'AUC observée est de **{row['Mean AUC (95% CI)']}**, indiquant une bonne capacité de discrimination du modèle."),
        html.Li(f"**Sensibilité** : La sensibilité moyenne est de **{row['Mean Sensitivity (95% CI)']}**, suggérant que le modèle détecte efficacement les vrais positifs."),
        html.Li(f"**Spécificité** : La spécificité moyenne est de **{row['Mean Specificity (95% CI)']}**, indiquant que le modèle identifie correctement les vrais négatifs."),
        html.Li(f"**Significativité Statistique** : La p-value est de **{row['p-value']}**, confirmant que les performances du modèle sont statistiquement significatives et supérieures au hasard. Leur manque de variance peut s'expliquer par le faible nombre de permutations utilisées lors du test.")
    ]
    
    # Ajouter une conclusion
    interpretation_list.append(
        html.Li(f"Ces résultats démontrent que le modèle est performant pour classifier **{disorder}** par rapport aux sujets sains.")
    )
    
    return html.Ul(interpretation_list, style={"fontSize": "16px", "marginLeft": "20px"})

# ----- LAYOUT -----
app.layout = html.Div([
    html.H1("Dashboard Interactif - Pathologies EEG", style={"textAlign": "center"}),
    
    # Introduction
    html.Div([
        html.H2("Introduction"),
        html.Ul([
            html.Li("**Band et Metric** : Type de bande de fréquences EEG et la métrique associée (AB = PSD (Power Spectral Density) et COH = Cohérence)."),
            html.Li("**Mean AUC (95% CI)** : Aire sous la courbe moyenne et son intervalle de confiance à 95 %."),
            html.Li("**Mean Sensitivity & Mean Specificity (95% CI)** : Sensibilité et spécificité moyennes avec leurs IC à 95 %."),
            html.Li("**p-value** : Reflète la significativité statistique (test de permutation) pour déterminer si la performance est au-dessus du hasard."),
            html.Li("**Healthy Control** : Groupe témoin pour comparer avec les différentes pathologies."),
        ], style={"marginLeft": "20px"}),
    ], style={"marginBottom": "20px", "padding": "20px", "backgroundColor": "#f0f8ff", "borderRadius": "5px"}),
    
    # Sélection de la pathologie
    html.Div([
        html.Label("Sélectionnez une pathologie :", style={"fontSize": "18px"}),
        dcc.Dropdown(
            id="disorder-dropdown",
            options=[
                {"label": disorder, "value": disorder}
                for disorder in df["main.disorder"].unique() if disorder != "Healthy Control"
            ],
            value=df["main.disorder"].unique()[0],  # Valeur par défaut
            placeholder="Sélectionnez une pathologie",
            style={"fontSize": "16px"}
        )
    ], style={"width": "50%", "margin": "0 auto", "marginBottom": "20px"}),
    
    # Mise en page côte à côte (tableau à gauche, barplot à droite)
    html.Div([
        # Colonne de gauche : tableau
        html.Div([
            html.H2("Tableau des résultats filtrés", style={"textAlign": "center"}),
            dash_table.DataTable(
                id="filtered-table",
                style_table={
                    "overflowX": "auto",
                    "width": "100%",
                    "maxHeight": "400px",
                    "border": "1px solid #ddd",
                    "borderRadius": "5px"
                },
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold",
                    "textAlign": "center"
                },
                style_cell={
                    "textAlign": "left",
                    "padding": "5px",
                    "fontSize": "14px"
                },
                style_data={
                    "whiteSpace": "normal",
                    "height": "auto",
                },
                page_size=10,  # Nombre de lignes par page
            ),
        ], style={
            "width": "45%",
            "display": "inline-block",
            "verticalAlign": "top",
            "marginRight": "5%"
        }),
    
        # Colonne de droite : barplot
        html.Div([
            html.H2("Barplot des effectifs", style={"textAlign": "center"}),
            dcc.Graph(id="barplot", style={"height": "500px"}),
        ], style={
            "width": "45%",
            "display": "inline-block",
            "verticalAlign": "top"
        }),
    ], style={"padding": "0 20px"}),
    
    # Section pour l'interprétation
    html.Div([
        html.H2("Interprétation des Résultats", style={"textAlign": "center"}),
        html.Div(id="interpretation-text", style={
            "marginTop": "20px",
            "fontSize": "16px",
            "padding": "20px",
            "backgroundColor": "#f9f9f9",
            "borderRadius": "5px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
        })
    ], style={"marginTop": "40px", "padding": "0 20px"})
])

# ----- CALLBACK -----
@app.callback(
    [
        Output("barplot", "figure"),
        Output("filtered-table", "data"),
        Output("filtered-table", "columns"),
        Output("interpretation-text", "children")  # Sortie pour l'interprétation
    ],
    [Input("disorder-dropdown", "value")]
)
def update_dashboard(selected_disorder):
    """
    Met à jour le barplot (effectifs), le tableau (final_results_df),
    et l'interprétation basée sur la pathologie sélectionnée.
    """
    # Filtrer les données pour le barplot
    filtered_counts = count_data[count_data["main.disorder"].isin(["Healthy Control", selected_disorder])]
    
    # Générer le barplot
    barplot = px.bar(
        filtered_counts,
        x="main.disorder",
        y="Count",
        text="Count",
        title=f"Effectifs - Healthy Control vs {selected_disorder}",
        labels={"main.disorder": "Catégorie", "Count": "Effectif"},
        color="main.disorder",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    barplot.update_layout(title_x=0.5, height=500, plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9")
    # Rendre les barres plus fines
    barplot.update_traces(width=0.3, textposition="outside", marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    # Filtrer le DataFrame final pour la pathologie sélectionnée
    filtered_df = final_results_df[final_results_df["main.disorder"] == selected_disorder]
    
    # Colonnes du tableau
    columns = [{"name": col, "id": col} for col in filtered_df.columns]
    
    # Interprétation
    interpretation = generate_interpretation(filtered_df, selected_disorder)
    
    return (
        barplot,
        filtered_df.to_dict("records"),
        columns,
        interpretation
    )

# ----- LANCER L'APPLICATION -----
if __name__ == "__main__":
    app.run_server(debug=True)

