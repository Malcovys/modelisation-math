from core.linear_system import solve_linear_system
from core.linear_programmation import lp_maximize_from_csv, lp_minimize_from_csv

from typing import List
import os


# a: List[List[float]] = [
#     [2,   25,  5],
#     [10,   0, 30],
#     [0.5, 10,  1]
# ]

# b = [50, 100, 20]

# solutions = solve_linear_system(a, b)

# if(solutions is None):
#     print("Undetermined solution")
# else:
#     print(solutions)

currend_directory = os.path.dirname(os.path.abspath(__file__))

# pastry_data__path = os.path.join(currend_directory, "./data/csv/pastry.csv")
# max_result = lp_maximize_from_csv(
#     path=data_path, 
#     problem_name="Pastry",
#     to_maximize="Benefits",
#     decision_var_col="Products"
# )

# print(f"max solution: {max_result}")

transport_data__path = os.path.join(currend_directory, "./data/csv/transport.csv")
min_result = lp_minimize_from_csv(
    path=transport_data__path, 
    problem_name=None,
    to_minimize="Cost",
    decision_var_col="Ingrédient"
)

print(f"min solution: {min_result}")