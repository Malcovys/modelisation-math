import streamlit as st
import pandas as pd
import tempfile
import os
from core.linear_programmation import lp_solve, lp_maximize_from_csv, lp_minimize_from_csv


def show():
    """
    Page principale pour la programmation linéaire.
    Gère à la fois l'import CSV et la saisie manuelle.
    """
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
        
        input_mode = st.radio(
            "Mode de saisie :",
            ["📁 Import CSV", "✍️ Saisie manuelle"],
            horizontal=True
        )
        
        if input_mode == "📁 Import CSV":
            uploaded_file = st.file_uploader(
                "Choisissez un fichier CSV",
                type=['csv'],
                help="Format : Products, Resources..., Objective"
            )
            
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.markdown("**Aperçu des données :**")
                st.dataframe(df, use_container_width=True)
                
                # Sélection des colonnes
                col_decision = st.selectbox("Colonne des variables de décision", df.columns, index=0)
                col_objective = st.selectbox("Colonne objectif", df.columns, index=len(df.columns)-1)
            
            solve_btn = st.button("🔍 Résoudre", type="primary", use_container_width=True)
        
        else:  # Saisie manuelle
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
            
            st.markdown("**Limites (RHS)**")
            st.caption("Valeurs séparées par des virgules")
            rhs_text = st.text_input(
                "RHS",
                value="50, 60",
                label_visibility="collapsed",
                key="lp_rhs"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                solve_btn = st.button("🔍 Résoudre", type="primary", use_container_width=True)
            with col_btn2:
                clear_btn = st.button("🗑️ Effacer", use_container_width=True)
    
    # Colonne 2 : Résultats
    with col2:
        st.subheader("📊 Résultats")
        
        if input_mode == "📁 Import CSV" and solve_btn:
            if uploaded_file is not None:
                try:
                    # Sauvegarder temporairement le fichier
                    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Résoudre
                    if problem_type == "Maximisation":
                        result = lp_maximize_from_csv(tmp_path, "LP_Problem", col_objective, col_decision)
                    else:
                        result = lp_minimize_from_csv(tmp_path, "LP_Problem", col_objective, col_decision)
                    
                    # Nettoyer le fichier temporaire
                    os.unlink(tmp_path)
                    
                    # Afficher les résultats
                    st.success(f"✅ Problème de {problem_type.lower()} résolu !")
                    
                    for var, val in result.items():
                        st.metric(label=var, value=f"{val:.4f}")
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.warning("⚠️ Veuillez charger un fichier CSV")
        
        elif input_mode == "✍️ Saisie manuelle" and solve_btn:
            try:
                # Parser les données
                obj_coef = [float(x.strip()) for x in objective_text.split(',')]
                
                constr_lines = constraints_text.strip().split('\n')
                constr_coef = [[float(x) for x in line.split()] for line in constr_lines if line.strip()]
                
                rhs = [float(x.strip()) for x in rhs_text.split(',')]
                
                # Variables de décision
                decision_vars = [f"x{i+1}" for i in range(len(obj_coef))]
                
                # Résoudre
                result = lp_solve(
                    problem_name="LP_Problem",
                    decision_vars=decision_vars,
                    decision_vars_coef=obj_coef,
                    constraintes_coef=constr_coef,
                    constraintes_inequality=rhs,
                    maximize=(problem_type == "Maximisation")
                )
                
                # Afficher les résultats
                st.success(f"✅ Problème de {problem_type.lower()} résolu !")
                
                for var, val in result.items():
                    st.metric(label=var, value=f"{val:.4f}")
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        else:
            st.info("👈 Entrez les données et cliquez sur 'Résoudre'")
        
        