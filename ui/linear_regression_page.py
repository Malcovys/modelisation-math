import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show():
    st.header("📈 Régression Linéaire")
    st.markdown("Analyse de régression et prédiction")
    
    # Mode de saisie
    input_mode = st.radio(
        "Mode de saisie :",
        ["✍️ Saisie manuelle", "📁 Import CSV"],
        horizontal=True
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Saisie des données")
        
        if input_mode == "✍️ Saisie manuelle":
            st.markdown("**Valeurs X**")
            st.caption("Valeurs séparées par des virgules")
            x_text = st.text_input(
                "X",
                value="1, 2, 3, 4, 5",
                label_visibility="collapsed",
                key="reg_x"
            )
            
            st.markdown("**Valeurs Y**")
            st.caption("Valeurs séparées par des virgules")
            y_text = st.text_input(
                "Y",
                value="2, 4, 5, 4, 5",
                label_visibility="collapsed",
                key="reg_y"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                compute_btn = st.button("📊 Calculer", type="primary", use_container_width=True)
            with col_btn2:
                clear_btn = st.button("🗑️ Effacer", use_container_width=True)
        
        else:  # Import CSV
            uploaded_file = st.file_uploader(
                "Choisissez un fichier CSV",
                type=['csv'],
                help="Format : deux colonnes X et Y",
                key="reg_csv"
            )
            
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.markdown("**Aperçu des données :**")
                st.dataframe(df, use_container_width=True)
            
            compute_btn = st.button("📊 Calculer", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Résultats")
        
        if input_mode == "✍️ Saisie manuelle" and compute_btn:
            try:
                # Parser les données
                x = [float(val.strip()) for val in x_text.split(',')]
                y = [float(val.strip()) for val in y_text.split(',')]
                
                if len(x) != len(y):
                    st.error("❌ X et Y doivent avoir le même nombre d'éléments")
                else:
                    # Calculer et afficher la régression
                    _compute_and_display_regression(x, y)
                    
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        
        elif input_mode == "📁 Import CSV" and compute_btn:
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    x = df.iloc[:, 0].values.tolist()
                    y = df.iloc[:, 1].values.tolist()
                    
                    # Calculer et afficher la régression
                    _compute_and_display_regression(x, y)
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.warning("⚠️ Veuillez charger un fichier CSV")
        else:
            st.info("👈 Entrez les données et cliquez sur 'Calculer'")


def _compute_and_display_regression(x, y):
    """Fonction auxiliaire pour calculer et afficher les résultats de régression"""
    # Calculer la régression
    x_array = np.array(x)
    y_array = np.array(y)
    
    # Calcul simple avec numpy
    n = len(x_array)
    x_mean = np.mean(x_array)
    y_mean = np.mean(y_array)
    
    a = np.sum((x_array - x_mean) * (y_array - y_mean)) / np.sum((x_array - x_mean) ** 2)
    b = y_mean - a * x_mean
    
    # R²
    y_pred = a * x_array + b
    ss_res = np.sum((y_array - y_pred) ** 2)
    ss_tot = np.sum((y_array - y_mean) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    # Afficher les résultats
    st.success("✅ Régression calculée !")
    
    st.metric("Équation", f"y = {a:.4f}x + {b:.4f}")
    
    col_a, col_b, col_r2 = st.columns(3)
    with col_a:
        st.metric("Pente (a)", f"{a:.4f}")
    with col_b:
        st.metric("Ordonnée (b)", f"{b:.4f}")
    with col_r2:
        st.metric("R²", f"{r2:.4f}")
    
    # Graphique
    st.markdown("**Graphique**")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Nuage de points
    ax.scatter(x, y, color='blue', label='Données', s=50, alpha=0.6)
    
    # Droite de régression
    x_line = np.linspace(min(x), max(x), 100)
    y_line = a * x_line + b
    ax.plot(x_line, y_line, color='red', label=f'y = {a:.2f}x + {b:.2f}', linewidth=2)
    
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('Régression Linéaire', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
