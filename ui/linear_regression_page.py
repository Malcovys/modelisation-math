import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from core.linear_regression import linear_regression_compute

def display_data_points_cloud_graphic(
    X_data: list[float],
    X_label: str,
    Y_data: list[float],
    Y_lable: str
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(
        X_data, 
        Y_data, 
        color='blue', 
        label='Données', 
        s=50, 
        alpha=0.6
    )
    
    ax.set_xlabel(f"{X_label}(X)", fontsize=12)
    ax.set_ylabel(f"{Y_lable} (Y)", fontsize=12)

    ax.set_title('Nuage de points', fontsize=14, fontweight='bold')

    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

def display_regressionline(
        a: float, 
        b: float,
        X_data: list[float],
        X_label: str,
        Y_data: list[float],
        Y_lable: str
) -> None:
    st.markdown("**Graphique**")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Points cloud
    ax.scatter(
        X_data, 
        Y_data, 
        color='blue', 
        label='Données', 
        s=50, 
        alpha=0.6
    )   
    
    # Regression line
    x_line = np.linspace(min(X_data), max(X_data), 100)
    y_line = a * x_line + b
    ax.plot(
        x_line, 
        y_line, 
        color='green', 
        label=f'y = {a:.3f}x + {b:.3f}', 
        linewidth=2
    )
    
    ax.set_xlabel(f"{X_label}(X)", fontsize=12)
    ax.set_ylabel(f"{Y_lable} (Y)", fontsize=12)

    ax.set_title("Droite de regression linéaire", fontsize=14, fontweight='bold')

    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

def show():
    st.header("📈 Régression Linéaire")
    st.markdown("Analyse de régression et prédiction")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Saisie des données")
        
        # Csv uploader
        uploaded_file = st.file_uploader(
            "Choisissez un fichier CSV",
            type=['csv'],
            help="Format : deux colonnes X et Y",
            key="reg_csv"
        )

        compute_btn = st.button("📊 Calculer", type="primary", width="stretch")
        
        if uploaded_file is not None:
            # Load csv data
            data_frame = pd.read_csv(uploaded_file)

            # Select explicative and tager col
            explicative_col = st.selectbox(
                "Colonne des variables explicative", 
                data_frame.columns, 
                index=0
            )
            target_col = st.selectbox(
                "Colonne des variables à expliquer", 
                data_frame.columns, 
                index=len(data_frame.columns)-1
            )
            
            # Extract data
            explicative_vars = data_frame[explicative_col].tolist()
            target_vars = data_frame[target_col].tolist()

            # Data preview
            st.markdown("**Aperçu des données :**")

            
            # Points clound
            display_data_points_cloud_graphic(
                X_data=explicative_vars, 
                X_label=explicative_col,
                Y_data=target_vars, 
                Y_lable=target_col
            )
            
            # Table
            st.dataframe(data_frame, width="stretch")
    
    with col2:
        st.subheader("📊 Résultats")
        
        if compute_btn:
            if uploaded_file is not None:
                try:
                    # Calculate the linear model
                    result = linear_regression_compute(
                        explicative_vars=explicative_vars, 
                        tagert_vars=target_vars
                    )
                    a = result["a"]
                    b = result["b"]
                    correlation = result["correlation"]

                    # Display result
                    st.success("✅ Régression calculée !")

                    st.metric("Équation", f"y = {a:.3f}x + {b:.3f}")

                    # Correlation
                    col_corr1, col_corr2 = st.columns([2, 3])
                    with col_corr1:
                        st.metric("Corrélation ", f"{correlation:.3f}")
                    
                    with col_corr2:
                        # Déterminer la force de la corrélation
                        abs_corr = abs(correlation)
                        if abs_corr >= 0.8:
                            st.success("🟢 Très forte corrélation")
                        elif abs_corr >= 0.6:
                            st.info("🟢 Forte corrélation")
                        elif abs_corr >= 0.4:
                            st.warning("🟠 Corrélation modérée")
                        else:
                            st.error("🔴 Faible corrélation")

                    display_regressionline(
                        a=result["a"],
                        b=result["b"],
                        X_data=explicative_vars, 
                        X_label=explicative_col,
                        Y_data=target_vars, 
                        Y_lable=target_col
                    )
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.warning("⚠️ Veuillez charger un fichier CSV")
        else:
            st.info("👈 Entrez les données et cliquez sur 'Calculer'")