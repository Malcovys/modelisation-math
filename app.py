import streamlit as st

# Import des pages
from ui import linear_system_page
from ui import linear_programming_page
from ui import regression_page
from ui import stochastic_page

# Configuration de la page
st.set_page_config(
    page_title="Application de Modélisation Mathématique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("📐 Application de Modélisation Mathématique")
st.markdown("---")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
module = st.sidebar.radio(
    "Choisissez un module :",
    [
        "📐 Systèmes Linéaires",
        "📊 Programmation Linéaire",
        "📈 Régression Linéaire",
        "🎲 Processus Stochastique"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Application de résolution et modélisation mathématique**

Développée avec Streamlit et NumPy

**Modules disponibles :**
- Systèmes linéaires
- Programmation linéaire
- Régression linéaire
- Processus stochastique
""")

# Afficher la page sélectionnée
if module == "📐 Systèmes Linéaires":
    linear_system_page.show()

elif module == "📊 Programmation Linéaire":
    linear_programming_page.show()

elif module == "📈 Régression Linéaire":
    regression_page.show()

elif module == "🎲 Processus Stochastique":
    stochastic_page.show()
