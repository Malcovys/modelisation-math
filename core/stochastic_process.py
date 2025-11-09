import numpy as np

def stochastic_process_simule_markov_chain(
    # states: list[str],
    transition_matrix: list[list[float]],
    initial_distribution: list[float],
    target_time: int
) -> list[list[float]]:
    # Validate dimensions
    if len(transition_matrix) != len(initial_distribution):
        raise ValueError("The size of the initial distribution must match to the size of the transition matrix.")

    # Validate that the transition matrix
    for row in transition_matrix:
        if not np.isclose(sum(row), 1.0):
            raise ValueError("Each row of the transition matrix must sum to 1.")

    # Validate that the initial distribution
    if not np.isclose(sum(initial_distribution), 1.0):
        raise ValueError("The initial distribution must sum to 1.")
    
    trans_matrix = np.array(transition_matrix)
    dist_evolutions: list[list[float]] = [initial_distribution]

    # Simulation
    for i in range(target_time):
        dist = np.matmul(dist_evolutions[i], trans_matrix)
        dist_evolutions.append(dist.tolist())

    return dist_evolutions


def stochastic_process_simule_random_walk_with_markov_chain():
    pass


def stochastic_process_simule_random_walk(
    states: list[str],
    probabilities: list[float],
    step: int
) -> list[str]:
    if len(states) != len(probabilities):
        raise ValueError("The number of states must match the size of the probabilities.")

    # Validate that the probabilities distribution
    if not np.isclose(sum(probabilities), 1.0):
        raise ValueError("The probabilities distribution must sum to 1.")
    
    # Validate that step
    if step <= 0:
        raise ValueError("The number of steps must be a positive integer.")
    
    # Simulation
    path_evolution: list[str] = []
    for _ in range(step):
        path_evolution.append(str(np.random.choice(states, p=probabilities)))

    return path_evolution


# transition_matrix = [
#     [0.6, 0.3, 0.1],
#     [0.4, 0.4, 0.2],
#     [0.0, 0.0, 1.0]
# ]

# initial_distibution = [0.7, 0.2, 0.1]
# states = ["A", "I", "P"]

# result = stochastic_process_simule_markov_chain(
#     states=states,
#     transition_matrix=transition_matrix,
#     initial_distribution=initial_distibution,
#     target_time=2
# )

# print(result)


# states = ["A", "B", "C"]
# probabilities = [0.2, 0.5, 0.3]

# result = stochastic_process_simule_random_walk(
#     states=states,
#     probabilities=probabilities,
#     step=5
# )

# print(result)