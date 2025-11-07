import streamlit as st
import numpy as np
import pandas as pd

def show():
    """Page pour la résolution de systèmes linéaires"""
    st.header("📐 Résolution de Systèmes Linéaires")
    st.markdown("Résolution de systèmes d'équations linéaires de la forme **Ax = b**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Saisie des données")
        
        # Saisie de la matrice A
        st.markdown("**Matrice A (coefficients)**")
        st.caption("Entrez chaque ligne sur une nouvelle ligne, coefficients séparés par des espaces")
        matrix_a_text = st.text_area(
            "Matrice A",
            value="2 1 -4\n3 3 -5\n4 5 -2",
            height=150,
            label_visibility="collapsed",
            key="matrix_a"
        )
        
        # Saisie du vecteur b
        st.markdown("**Vecteur b (résultats)**")
        st.caption("Valeurs séparées par des virgules")
        vector_b_text = st.text_input(
            "Vecteur b",
            value="6, 12, 10",
            label_visibility="collapsed",
            key="vector_b"
        )
        
        # Boutons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            solve_btn = st.button("🔍 Résoudre", type="primary", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Effacer", use_container_width=True)
    
    with col2:
        st.subheader("📊 Résultats")
        
        if clear_btn:
            st.info("Données effacées. Entrez de nouvelles valeurs.")
        
        elif solve_btn:
            try:
                # Parser la matrice A
                lines = matrix_a_text.strip().split('\n')
                a = [[float(x) for x in line.split()] for line in lines if line.strip()]
                
                # Parser le vecteur b
                b = [float(x.strip()) for x in vector_b_text.split(',')]
                
                # Vérifier les dimensions
                if len(a) != len(b):
                    st.error(f"❌ Erreur : La matrice A a {len(a)} lignes mais le vecteur b a {len(b)} éléments.")
                else:
                    # Résoudre le système
                    from core.linear_system import solve_linear_system
                    solution = solve_linear_system(a, b)
                    
                    # Afficher les résultats
                    st.success("✅ Système résolu avec succès !")
                    
                    st.markdown("**Solution :**")
                    for i, val in enumerate(solution):
                        st.metric(label=f"x{i+1}", value=f"{val:.6f}")
                    
                    # Vérification (optionnel)
                    st.markdown("**Vérification : Ax**")
                    a_array = np.array(a)
                    x_array = np.array(solution)
                    b_calculated = a_array @ x_array
                    
                    verification_df = pd.DataFrame({
                        'b (donné)': b,
                        'Ax (calculé)': b_calculated,
                        'Différence': [abs(b[i] - b_calculated[i]) for i in range(len(b))]
                    })
                    st.dataframe(verification_df, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la résolution : {str(e)}")
        else:
            st.info("👈 Entrez les données et cliquez sur 'Résoudre'")
