from core.linear_system import solve_linear_system
from typing import List

a: List[List[float]] = [
    [2,   25,  5],
    [10,   0, 30],
    [0.5, 10,  1]
]

b = [50, 100, 20]

solutions = solve_linear_system(a, b)

if(solutions is None):
    print("Undetermined solution")
else:
    print(solutions)