import streamlit as st
import pandas as pd
import tempfile
import os
from core.linear_programmation import lp_solve, lp_maximize_from_csv, lp_minimize_from_csv

input_modes = [
    "📁 Import CSV",
    "✍️ Saisie manuelle"
]

def show():
    # === header section ====
    st.header("📊 Programmation Linéaire")
    st.markdown("Optimisation linéaire (maximisation ou minimisation)")

    # Type de problème
    problem_type = st.radio(
        "Type de problème :",
        ["Maximisation", "Minimisation"],
        horizontal=True
    )
    
    # Disposition en 2 colonnes
    col1, col2 = st.columns([1, 1])
    
    # Colonne 1 : Saisie des données
    with col1:
        st.subheader("📥 Saisie des données")
        
        # Choise between CSV or manual
        input_mode = st.radio(
            "Mode de saisie :",
            input_modes,
            horizontal=True
        )
        
        if input_mode == input_modes[0]: # CSV input mode
            # Uploader
            uploaded_file = st.file_uploader(
                "Choisissez un fichier CSV",
                type=['csv'],
                help="Format : Products, Resources..., Objective"
            )

            # Choose decision variables col selection
            if uploaded_file is not None:
                # Display uploaded data content
                data_frame = pd.read_csv(uploaded_file)

                col_decision = st.selectbox("Colonne des variables de décision", data_frame.columns, index=0)
                col_objective = st.selectbox("Colonne objectif", data_frame.columns, index=len(data_frame.columns)-1)
            
            # Resolve button
            solve_btn = st.button("🔍 Résoudre", type="primary", width="stretch")

            if uploaded_file is not None:
                st.markdown("**Aperçu des données :**")
                st.dataframe(data_frame, width="stretch")
        
        else:  # Manuel input
            st.markdown("**Fonction objectif (coefficients)**")
            st.caption("Coefficients séparés par des virgules")
            objective_text = st.text_input(
                "Objectif",
                value="5, 4",
                label_visibility="collapsed",
                key="lp_objective"
            )
            
            st.markdown("**Contraintes (matrice)**")
            st.caption("Une contrainte par ligne, coefficients séparés par des espaces")
            constraints_text = st.text_area(
                "Contraintes",
                value="2 3\n1 2",
                height=100,
                label_visibility="collapsed",
                key="lp_constraints"
            )
            
            st.markdown("**Limites des contraintes (ressources disponibles)**")
            st.caption("Valeurs séparées par des virgules")
            avalibles_resources_text = st.text_input(
                "Ressources disponibles",
                value="50, 60",
                label_visibility="collapsed",
                key="lp_avalibles_resources"
            )

            # Resolve button
            solve_btn = st.button("🔍 Résoudre", type="primary", width="stretch")
    
    # Colonne 2 : Results
    with col2:
        st.subheader("📊 Résultats")
        
        if input_mode == input_modes[0] and solve_btn:
            if uploaded_file is not None:
                try:
                    # Save temporary data file
                    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Resolve
                    if problem_type == "Maximisation":
                        result = lp_maximize_from_csv(tmp_path, col_objective, col_decision)
                    else:
                        result = lp_minimize_from_csv(tmp_path, col_objective, col_decision)
                    
                    # Clear temporary file
                    os.unlink(tmp_path)
                    
                    # Display result
                    st.success(f"✅ Problème de {problem_type.lower()} résolu !")
                    
                    for var, val in result.items():
                        st.metric(label=var, value=f"{val:.4f}")
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.warning("⚠️ Veuillez charger un fichier CSV")
        
        elif input_mode == input_modes[1] and solve_btn:
            try:
                # Parse data
                obj_coef = [float(x.strip()) for x in objective_text.split(',')]
                
                constr_lines = constraints_text.strip().split('\n')
                constr_coef = [[float(x) for x in line.split()] for line in constr_lines if line.strip()]
                
                avalibles_resources = [float(x.strip()) for x in avalibles_resources_text.split(',')]
                
                # Decision variables
                decision_vars = [f"x{i+1}" for i in range(len(obj_coef))]
                
                # Resolve
                result = lp_solve(
                    decision_vars=decision_vars,
                    decision_vars_coef=obj_coef,
                    constraintes_coef=constr_coef,
                    constraintes_inequality=avalibles_resources,
                    maximize=(problem_type == "Maximisation")
                )
                
                # Display result
                st.success(f"✅ Problème de {problem_type.lower()} résolu !")
                
                for var, val in result.items():
                    st.metric(label=var, value=f"{val:.4f}")
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        else:
            st.info("👈 Entrez les données et cliquez sur 'Résoudre'")
        
        