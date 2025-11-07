import streamlit as st

from ui import linear_system_page, linear_programming_page, regression_page, stochastic_page

# Page Configuration
st.set_page_config(
    page_title="Modélisation Mathématique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("Modules")
module = st.sidebar.radio(
    "",
    [
        "📐 Systèmes Linéaires",
        "📊 Programmation Linéaire",
        "📈 Régression Linéaire",
        "🎲 Processus Stochastique"
    ]
)

# Afficher la page sélectionnée
if module == "📐 Systèmes Linéaires":
    linear_system_page.show()

elif module == "📊 Programmation Linéaire":
    linear_programming_page.show()

elif module == "📈 Régression Linéaire":
    regression_page.show()

elif module == "🎲 Processus Stochastique":
    stochastic_page.show()