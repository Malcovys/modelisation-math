import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import graphviz

from core.stochastic_process import stochastic_process_simule_markov_chain, stochastic_process_simule_random_walk

# Modularized function to display Markov Chain
def display_markov_chain(
    states: list[str],
    transition_matrix: list[list[float]]
) -> None:
    dot = graphviz.Digraph()

    for i, state in enumerate(states):
        dot.node(str(i), state)

    for i, row in enumerate(transition_matrix):
        for j, prob in enumerate(row):
            if prob > 0:
                dot.edge(str(i), str(j), label=f"{prob:.4f}")

    st.graphviz_chart(dot)

def display_markov_distributions_evolution_graph(
    states: list[str],
    distributions_evolution: list[list[float]]
) -> None:
    """Affiche l'évolution des distributions sous forme de graphique en ligne."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Tracer une courbe pour chaque état
    for i, state in enumerate(states):
        state_probabilities = [dist[i] for dist in distributions_evolution]
        ax.plot(
            range(len(distributions_evolution)),
            state_probabilities,
            marker='o',
            label=f"État {state}",
            linewidth=2
        )
    
    ax.set_xlabel("Temps (t)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Probabilité", fontsize=12, fontweight="bold")
    ax.set_title("Évolution des distributions au fil du temps", fontsize=14, fontweight="bold")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.0, 1.0)
    
    st.pyplot(fig)

def parse_states(states_text: str) -> list[str]:
    return [state.strip() for state in states_text.split(",")]

def parse_transition_matrix(matrix_text: str) -> list[list[float]]:
    lines = matrix_text.strip().split('\n')
    return [[float(x) for x in line.split()] for line in lines if line.strip()]

def parse_initial_distribution(initial_distribution_text: str) -> list[float]:
    return [float(x.strip()) for x in initial_distribution_text.split(",")]

def show():
    st.header("🎲 Processus Stochastique")
    st.markdown("Simulation de chaînes de Markov et marches aléatoires")

    process_type = st.radio(
        "Type de processus :",
        ["Chaîne de Markov", "Marche aléatoire"],
        horizontal=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📥 Paramètres")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            simulate_btn = st.button("🎲 Simuler", type="primary", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Effacer", use_container_width=True)

        if process_type == "Chaîne de Markov":
            st.markdown("**États**")
            st.caption("Noms des états séparés par des virgules")
            states_input = st.text_input(
                "États", 
                value="A, I, P", 
                label_visibility="collapsed", 
                key="markov_states"
            )

            st.markdown("**Matrice de transition d'état**")
            st.caption("Une ligne par état, probabilités séparées par des espaces")
            transition_matrix_input = st.text_area(
                "Matrice", 
                value="0.6 0.3 0.1\n0.4 0.4 0.2\n0.0 0.0 1.0", 
                height=100, 
                label_visibility="collapsed", 
                key="markov_matrix"
            )

            st.markdown("**Distribution initiale**")
            st.caption("Probabilités séparées par des virgules")
            initial_distribution_input = st.text_input(
                "État initial", 
                value="0.7, 0.2, 0.1", 
                label_visibility="collapsed", 
                key="markov_initial"
            )

            target_time_input = st.number_input(
                "Temps cible", 
                min_value=1, 
                max_value=100, 
                value=2, 
                key="markov_steps"
            )

            st.subheader("**Représentation de la chaîne de Markov**")
            try:
                states = parse_states(states_input)
                transition_matrix = parse_transition_matrix(transition_matrix_input)
                initial_distribution = parse_initial_distribution(initial_distribution_input)

                if len(states) != len(transition_matrix):
                    st.error("❌ Le nombre d'états doit correspondre à la taille de la matrice de transition.")
                else:
                    display_markov_chain(states, transition_matrix)
            except Exception as e:
                st.error(f"❌ Erreur dans les paramètres : {str(e)}")

        else:  # Marche aléatoire
            steps = st.number_input("Nombre de pas", min_value=1, max_value=1000, value=100, key="walk_steps")
            n_walks = st.number_input("Nombre de simulations", min_value=1, max_value=20, value=5, key="n_walks")
            p_up = st.slider("Probabilité d'aller vers le haut", min_value=0.0, max_value=1.0, value=0.5, step=0.05, key="p_up")

    with col2:
        st.subheader("📊 Résultats")

        if process_type == "Chaîne de Markov" and simulate_btn:
            try:
                distributions_evolution = stochastic_process_simule_markov_chain(
                    transition_matrix=transition_matrix,
                    initial_distribution=initial_distribution,
                    target_time=target_time_input
                )

                st.success("✅ Simulation terminée !")

                display_markov_distributions_evolution_graph(states, distributions_evolution)

                for i, distribution in enumerate(distributions_evolution):
                    st.metric(f"Distribution (t = {i})", str([round(x, 4) for x in distribution]))
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

        elif process_type == "Marche aléatoire" and simulate_btn:
            try:
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

                st.success("✅ Simulation terminée !")
                st.metric("Nombre de simulations", int(n_walks))
                st.metric("Nombre de pas", int(steps))

                final_positions = [walk[-1] for walk in walks]
                st.metric("Position finale moyenne", f"{np.mean(final_positions):.2f}")

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
