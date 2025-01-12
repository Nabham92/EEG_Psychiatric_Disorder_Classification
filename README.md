
---

## Modèles et méthodologie

Trois modèles principaux ont été utilisés pour la classification :

1. **Random Forest**
2. **Elastic Net (régression pénalisée)**
3. **Support Vector Machine (SVM)** avec optimisation de l'hyperparamètre `C` via une Grid Search.

Les performances des modèles ont été évaluées à l'aide d'une validation croisée à 10 plis. Les métriques calculées incluent l'AUC (Area Under the Curve), la sensibilité et la spécificité, avec des intervalles de confiance.

---

## Tableau de bord interactif

Un tableau de bord interactif permet de visualiser les performances des modèles pour chaque trouble psychiatrique et de comparer les résultats en fonction des bandes de fréquences et des métriques EEG. Ce tableau de bord est généré à l'aide du script Python `dashboard.py`.

---

## Référence de l'étude originale

Ce projet s'inspire partiellement de l'étude suivante :

- **Titre** : *Identification of Major Psychiatric Disorders From Resting-State Electroencephalography Using a Machine Learning Approach*  
- **Auteurs** : Su Mi Park, Boram Jeong, Da Young Oh, Chi-Hyun Choi, Hee Yeon Jung, Jun-Young Lee, Donghwan Lee, Jung-Seok Choi  
- **Publication** : Frontiers in Psychiatry, 2021  
- **Lien vers l'étude** : [Accéder à l'étude sur Frontiers](https://www.frontiersin.org/articles/10.3389/fpsyt.2021.707581/full)

**Note** : Les résultats obtenus dans ce projet peuvent différer de ceux de l'étude originale.

---

## Outils utilisés

- **Python** : pandas, numpy, sklearn, plotly, dash
- **Validation croisée** : StratifiedKFold
- **Optimisation** : GridSearchCV
- **Visualisation** : Matplotlib, Plotly
