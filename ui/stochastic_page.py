import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import graphviz

from core.stochastic_process import stochastic_process_simule_markov_chain, stochastic_process_simule_random_walk


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

def display_markov_distributions_evolution_line_graph(
    states: list[str],
    distributions_evolution: list[list[float]]
) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot a curve for each state
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

def display_walk_evolution_resume(states: list[str], evolution: list[str]) -> None:
    state_counts = {state: evolution.count(state) for state in states}

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de pas", len(evolution))
    with col2:
        most_visited = max(state_counts, key=lambda k: state_counts.get(k, 0))
        st.metric("État le plus visité", f"{most_visited} ({state_counts[most_visited]}x)")
    with col3:
        least_visited = min(state_counts, key=lambda k: state_counts.get(k, 0))
        st.metric("État le moins visité", f"{least_visited} ({state_counts[least_visited]}x)")


def display_walk_evolution_sequence(evolution: list[str]) -> None:
    sequence_text = " → ".join(evolution)
    st.code(sequence_text, language="text")

def display_walk_evolution_table_resume(states: list[str], evolution: list[str]) -> None:
    state_counts = {state: evolution.count(state) for state in states}
    
    stats_data = {
        "État": states,
        "Occurrences": [state_counts[state] for state in states],
        "Pourcentage": [f"{(state_counts[state]/len(evolution)*100):.2f}%" for state in states]
    }
    
    st.dataframe(stats_data, use_container_width=True)

def display_walk_evolution_bar_graph(states: list[str], evolution: list[str]) -> None:
    # Count occurrences of each state
    state_counts = {state: evolution.count(state) for state in states}
    
    # Display a bar graph of occurrences
    fig, ax = plt.subplots(figsize=(10, 5))
    
    labels = states
    counts = [state_counts[state] for state in labels]
    colors = plt.get_cmap('Set3')(np.linspace(0, 1, len(labels)))
    bars = ax.bar(labels, counts, color=colors, alpha=0.8, edgecolor='black')
    
    # Add values on the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel("États", fontsize=12, fontweight="bold")
    ax.set_ylabel("Nombre de visites", fontsize=12, fontweight="bold")
    ax.set_title("Distribution des visites par état", fontsize=14, fontweight="bold")

    ax.grid(True, alpha=0.3, axis='y')
    
    st.pyplot(fig)

def parse_states(states_text: str) -> list[str]:
    return [state.strip() for state in states_text.split(",")]

def parse_transition_matrix(matrix_text: str) -> list[list[float]]:
    lines = matrix_text.strip().split('\n')
    return [[float(x) for x in line.split()] for line in lines if line.strip()]

def parse_distribution(initial_distribution_text: str) -> list[float]:
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
            markorv_states_input = st.text_input(
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
                markov_states = parse_states(markorv_states_input)
                transition_matrix = parse_transition_matrix(transition_matrix_input)
                initial_distribution = parse_distribution(initial_distribution_input)

                if len(markov_states) != len(transition_matrix):
                    st.error("❌ Le nombre d'états doit correspondre à la taille de la matrice de transition.")
                else:
                    display_markov_chain(markov_states, transition_matrix)
            except Exception as e:
                st.error(f"❌ Erreur dans les paramètres : {str(e)}")

        else:  # Random walk
            walk_states_input = st.text_input(
                "États", 
                value="A, B, C", 
                label_visibility="collapsed", 
                key="walk_states"
            )

            walk_states_probility_input = st.text_input(
                "Probablité des états", 
                value="0.2, 0.5, 0.3",
                label_visibility="collapsed", 
                key="walk_prob"
            )

            walk_steps_input = st.number_input(
                "Nombre de pas", 
                min_value=1, 
                max_value=1000, 
                value=5, 
                key="walk_steps"
            )

            try:
                walk_states = parse_states(walk_states_input)
                walk_states_probility = parse_distribution(walk_states_probility_input)

                if len(walk_states) != len(walk_states_probility):
                    st.error("❌ Le nombre d'états doit correspondre au nombre des probabilitées.")

            except Exception as e:
                st.error(f"❌ Erreur dans les paramètres : {str(e)}")

    with col2:
        st.subheader("📊 Résultats")

        if process_type == "Chaîne de Markov" and simulate_btn:
            try:
                distributions_evolution: list[list[float]] = stochastic_process_simule_markov_chain(
                    transition_matrix=transition_matrix,
                    initial_distribution=initial_distribution,
                    target_time=target_time_input
                )

                st.success("✅ Simulation terminée !")

                display_markov_distributions_evolution_line_graph(markov_states, distributions_evolution)

                for i, distribution in enumerate(distributions_evolution):
                    st.metric(f"Distribution (t = {i})", str([round(x, 4) for x in distribution]))
            
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

        elif process_type == "Marche aléatoire" and simulate_btn:
            try:
                walk_evolution: list[str] = stochastic_process_simule_random_walk(
                    states=walk_states,
                    probabilities=walk_states_probility,
                    step=walk_steps_input
                )

                st.success("✅ Simulation terminée !")

                st.markdown("**Marches aléatoires**")
                display_walk_evolution_resume(walk_states, walk_evolution)

                st.markdown("**Séquence complète de la marche aléatoire**")
                display_walk_evolution_sequence(walk_evolution)

                display_walk_evolution_bar_graph(walk_states, walk_evolution)
                
                st.markdown("**Statistiques détaillées**")
                display_walk_evolution_table_resume(walk_states, walk_evolution)

            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
        else:
            st.info("👈 Configurez les paramètres et cliquez sur 'Simuler'")
