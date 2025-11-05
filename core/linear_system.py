import numpy as np
from typing import Sequence, Optional

def solve_linear_system(
    coefficient_matrix: Sequence[Sequence[float]], 
    ordinate_matrix: Sequence[float]
) -> Optional[Sequence[float]]:
    
    # Converte given arrays to a numpy arrays
    np_coefficient_matrix = np.array(coefficient_matrix, dtype=float)
    np_ordinate_matrix = np.array(ordinate_matrix, dtype=float)

    # Calculate coefficient matrix determinant
    coefficient_matrix_determinant: float = np.linalg.det(np_coefficient_matrix)    

    # If coefficient matrix determinant is equal to 0
    # the linear system solution is undetermined
    if np.isclose(coefficient_matrix_determinant, 0.0):
        return None
    
    # Solve the linear system and return results as python list
    solution = np.linalg.solve(np_coefficient_matrix, np_ordinate_matrix).tolist()

    # Round each value to 3 decimal places and convert numpy types to native floats
    return [float(round(x, 3)) for x in solution]
    
    

    
