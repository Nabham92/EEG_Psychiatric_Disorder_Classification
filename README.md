## Introduction

Ce projet vise à classifier des troubles psychiatriques majeurs en utilisant des données d'électroencéphalogramme (EEG) à l'état de repos, en appliquant des techniques avancées d'apprentissage automatique. En collaboration avec une équipe pluridisciplinaire, l'objectif est d'identifier des biomarqueurs EEG spécifiques permettant de distinguer efficacement les patients atteints de divers troubles psychiatriques des individus sains.

### Objectifs du Projet

- **Classification des Troubles Psychiatriques** : Développer et comparer des modèles de machine learning (Random Forest, Elastic Net, Support Vector Machine) pour classifier six catégories de troubles psychiatriques (schizophrénie, troubles de l'humeur, troubles liés au stress, troubles anxieux, troubles obsessionnels-compulsifs et troubles addictifs) contre des contrôles sains.
  
- **Analyse des Performances** : Évaluer les performances des modèles à l'aide de métriques telles que l'AUC, la sensibilité et la spécificité, en utilisant une validation croisée stratifiée à 10 plis pour assurer la robustesse des résultats.

- **Visualisation Interactive** : Créer un tableau de bord interactif permettant de visualiser les performances des modèles par pathologie, bande de fréquence EEG et métrique, facilitant ainsi l'interprétation des résultats et la prise de décision.

### Sources et Description des Données

Les données utilisées dans ce projet proviennent du fichier `EEG.machinelearing_data_BRMH.csv`, contenant des enregistrements EEG prétraités de 945 participants. Ces données incluent :

- **Variables Démographiques** : Âge, sexe, niveau d'éducation, QI.
  
- **Caractéristiques EEG** :
  - **Bandes de Fréquence** : Alpha, Beta, HighBeta, Gamma, Theta, Delta.
  - **Métriques** : Densité Spectrale de Puissance (PSD - AB) et Connectivité Fonctionnelle (FC - COH).

- **Labels de Classe** : `main.disorder`, indiquant le trouble psychiatrique majeur ou le contrôle sain.
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
