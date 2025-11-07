# Structure Modulaire de l'Application Streamlit

## 📁 Organisation des Fichiers

```
modelisation-math/
│
├── app.py                              ← Point d'entrée principal
│
├── ui/                                 ← Modules UI (pages)
│   ├── __init__.py
│   ├── linear_system_page.py          ← Page systèmes linéaires
│   ├── linear_programming_page.py     ← Page programmation linéaire
│   ├── regression_page.py             ← Page régression linéaire
│   └── stochastic_page.py             ← Page processus stochastique
│
├── core/                               ← Logique métier
│   ├── __init__.py
│   ├── linear_system.py
│   └── linear_programmation.py
│
└── data/csv/                           ← Données
    ├── pastry.csv
    └── ingredient.csv
```

## 🚀 Lancement de l'Application

```bash
# Activer l'environnement virtuel
source env/bin/activate  # Linux/Mac
# ou
.\env\Scripts\activate   # Windows

# Lancer l'application
streamlit run app.py
```

L'application s'ouvre à : **http://localhost:8501**

## 📄 Description des Fichiers

### `app.py` (Point d'entrée)
Fichier principal qui :
- Configure la page Streamlit
- Affiche la sidebar de navigation
- Route vers les différentes pages selon la sélection

### `ui/linear_system_page.py`
Module pour la résolution de systèmes linéaires :
- Saisie manuelle de matrices
- Résolution avec NumPy
- Affichage des résultats et vérification

### `ui/linear_programming_page.py`
Module pour la programmation linéaire :
- Import CSV ou saisie manuelle
- Maximisation/Minimisation
- Utilise `core/linear_programmation.py`

### `ui/regression_page.py`
Module pour la régression linéaire :
- Saisie manuelle ou CSV
- Calcul de a, b, R²
- Graphique avec Matplotlib

### `ui/stochastic_page.py`
Module pour les processus stochastiques :
- Chaînes de Markov
- Marches aléatoires
- Visualisations graphiques

## 🔧 Ajouter une Nouvelle Page

1. **Créer le fichier** dans `ui/` :
```python
# ui/ma_nouvelle_page.py
import streamlit as st

def show():
    st.header("Ma Nouvelle Page")
    # ... votre code ici
```

2. **Importer dans `app.py`** :
```python
from ui import ma_nouvelle_page
```

3. **Ajouter à la navigation** :
```python
module = st.sidebar.radio(
    "Choisissez un module :",
    [
        "📐 Systèmes Linéaires",
        "📊 Programmation Linéaire",
        "📈 Régression Linéaire",
        "🎲 Processus Stochastique",
        "🆕 Ma Nouvelle Page"  # Ajouter ici
    ]
)

# ...

elif module == "🆕 Ma Nouvelle Page":
    ma_nouvelle_page.show()
```

## ✅ Avantages de cette Structure

### 🎯 Modularité
- Chaque page est dans son propre fichier
- Facile à maintenir et déboguer
- Code réutilisable

### 🔍 Lisibilité
- Séparation claire des responsabilités
- Fichier principal court et simple
- Navigation intuitive

### 🚀 Scalabilité
- Facile d'ajouter de nouvelles pages
- Possibilité de travailler en équipe sur différentes pages
- Tests unitaires simplifiés

### 🔄 Réutilisabilité
- Fonctions auxiliaires facilement accessibles
- Import sélectif des modules nécessaires
- Pas de duplication de code

## 📝 Conventions de Code

### Nom des Fichiers
- Format : `nom_module_page.py`
- Tout en minuscules
- Underscores pour les espaces

### Structure d'une Page
```python
import streamlit as st
import numpy as np  # si nécessaire
import pandas as pd  # si nécessaire

def show():
    """Fonction principale de la page"""
    st.header("Titre de la Page")
    
    # ... code de la page

def _fonction_auxiliaire():
    """Fonction privée (préfixe _)"""
    # ... logique auxiliaire
```

### Gestion des États
- Utiliser `key` unique pour chaque widget
- Format : `"nom_page_widget"`
- Exemple : `key="reg_x"` pour le champ X de régression

## 🎨 Personnalisation

### Modifier le Thème
Créer `.streamlit/config.toml` :
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Ajouter des Icônes
Utilisez des émojis dans les titres :
```python
st.header("📊 Mon Titre")
st.sidebar.info("💡 Astuce...")
```

## 🐛 Débogage

### Afficher des Variables
```python
st.write("Debug:", ma_variable)
st.json(mon_dictionnaire)
```

### Vérifier l'État
```python
st.sidebar.write(st.session_state)
```

### Mode Développement
```bash
streamlit run app.py --logger.level=debug
```

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Galerie d'Applications](https://streamlit.io/gallery)
- [Forum Communautaire](https://discuss.streamlit.io/)

## 🤝 Contribution

Pour contribuer :
1. Créez une nouvelle branche
2. Ajoutez votre module dans `ui/`
3. Testez localement
4. Soumettez une pull request

---

**Bon développement ! 🚀**
