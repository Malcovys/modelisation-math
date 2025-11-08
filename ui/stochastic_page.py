import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show():
    """Page pour les processus stochastiques"""
    st.header("🎲 Processus Stochastique")
    st.markdown("Simulation de chaînes de Markov et marches aléatoires")
    
    # Type de processus
    process_type = st.radio(
        "Type de processus :",
        ["Chaîne de Markov", "Marche aléatoire"],
        horizontal=True
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Paramètres")
        
        if process_type == "Chaîne de Markov":
            st.markdown("**Matrice de transition**")
            st.caption("Une ligne par état, probabilités séparées par des espaces")
            matrix_text = st.text_area(
                "Matrice",
                value="0.7 0.3\n0.4 0.6",
                height=100,
                label_visibility="collapsed",
                key="markov_matrix"
            )
            
            st.markdown("**État initial**")
            st.caption("Probabilités séparées par des virgules")
            initial_text = st.text_input(
                "État initial",
                value="1, 0",
                label_visibility="collapsed",
                key="markov_initial"
            )
            
            steps = st.number_input("Nombre d'étapes", min_value=1, max_value=100, value=10, key="markov_steps")
            
        else:  # Marche aléatoire
            steps = st.number_input("Nombre de pas", min_value=1, max_value=1000, value=100, key="walk_steps")
            n_walks = st.number_input("Nombre de simulations", min_value=1, max_value=20, value=5, key="n_walks")
            p_up = st.slider("Probabilité d'aller vers le haut", min_value=0.0, max_value=1.0, value=0.5, step=0.05, key="p_up")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            simulate_btn = st.button("🎲 Simuler", type="primary", width="stretch")
        with col_btn2:
            clear_btn = st.button("🗑️ Effacer", width="stretch")
    
    with col2:
        st.subheader("📊 Résultats")
        
        if process_type == "Chaîne de Markov" and simulate_btn:
            try:
                # Parser les données
                lines = matrix_text.strip().split('\n')
                matrix = np.array([[float(x) for x in line.split()] for line in lines if line.strip()])
                
                initial = np.array([float(x.strip()) for x in initial_text.split(',')])
                
                # Simulation
                states = [initial]
                current_state = initial.copy()
                
                for _ in range(int(steps)):
                    current_state = current_state @ matrix
                    states.append(current_state.copy())
                
                # Résultats
                st.success("✅ Simulation terminée !")
                
                st.metric("État initial", str(initial))
                st.metric(f"État final (étape {int(steps)})", str(np.round(states[-1], 4)))
                
                # Graphique
                st.markdown("**Évolution de la chaîne de Markov**")
                fig, ax = plt.subplots(figsize=(10, 5))
                
                states_array = np.array(states)
                n_states = states_array.shape[1]
                
                for i in range(n_states):
                    ax.plot(states_array[:, i], label=f'État {i+1}', marker='o', markersize=4)
                
                ax.set_xlabel('Étapes', fontsize=12)
                ax.set_ylabel('Probabilité', fontsize=12)
                ax.set_title('Évolution de la Chaîne de Markov', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        
        elif process_type == "Marche aléatoire" and simulate_btn:
            try:
                # Simulation de marches aléatoires
                walks = []
                for _ in range(int(n_walks)):
                    positions = [0]
                    current_pos = 0
                    
                    for _ in range(int(steps)):
                        if np.random.random() < p_up:
                            current_pos += 1
                        else:
                            current_pos -= 1
                        positions.append(current_pos)
                    
                    walks.append(positions)
                
                # Résultats
                st.success("✅ Simulation terminée !")
                st.metric("Nombre de simulations", int(n_walks))
                st.metric("Nombre de pas", int(steps))
                
                # Statistiques
                final_positions = [walk[-1] for walk in walks]
                st.metric("Position finale moyenne", f"{np.mean(final_positions):.2f}")
                
                # Graphique
                st.markdown("**Marches aléatoires**")
                fig, ax = plt.subplots(figsize=(10, 5))
                
                for i, walk in enumerate(walks):
                    ax.plot(walk, alpha=0.6, label=f'Marche {i+1}')
                
                ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
                ax.set_xlabel('Étapes', fontsize=12)
                ax.set_ylabel('Position', fontsize=12)
                ax.set_title('Marches Aléatoires', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        else:
            st.info("👈 Configurez les paramètres et cliquez sur 'Simuler'")
