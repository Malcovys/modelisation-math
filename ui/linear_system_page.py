import streamlit as st
import numpy as np

from core.linear_system import solve_linear_system

def show():
    st.header("📐 Résolution de Systèmes Linéaires")
    st.markdown("Résolution de systèmes d'équations linéaires de la forme **Ax = b**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Saisie des données")
        
        # Set A matrix
        st.markdown("**Matrice A (coefficients)**")
        st.caption("Entrez chaque ligne sur une nouvelle ligne, coefficients séparés par des espaces")
        matrix_a_text = st.text_area(
            "Matrice A",
            value="2 1 -4\n3 3 -5\n4 5 -2",
            height=150,
            label_visibility="collapsed",
            key="matrix_a"
        )
        
        # Set vector b
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
                # Format A matrix
                lines = matrix_a_text.strip().split('\n')
                a = [[float(x) for x in line.split()] for line in lines if line.strip()]
                
                # Format vertor b
                b = [float(x.strip()) for x in vector_b_text.split(',')]
                
                # Check dimentions
                if len(a) != len(b):
                    st.error(f"❌ Erreur : La matrice A a {len(a)} lignes mais le vecteur b a {len(b)} éléments.")
                else:
                    # Resolve
                    solution = solve_linear_system(a, b)
                    
                    # Vérifier la solution retournée
                    if solution is None:
                        st.error("⚠️ La solution est indéterminée.")
                    else:
                        # Normaliser la solution en liste pour l'itération
                        solution_list = solution.tolist() if isinstance(solution, np.ndarray) else list(solution)
                        
                        # Afficher les résultats
                        st.success("✅ Système résolu avec succès !")
                        
                        st.markdown("**Solution :**")
                        for i, val in enumerate(solution_list):
                            st.metric(label=f"x{i+1}", value=f"{val}")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la résolution : {str(e)}")
        else:
            st.info("👈 Entrez les données et cliquez sur 'Résoudre'")
