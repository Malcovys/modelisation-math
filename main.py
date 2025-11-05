from core.linear_system import solve_linear_system

a = [[2, 1, -4], [3, 3, -5], [4, 5, -2]]
b = [8, 14, 16]

solutions = solve_linear_system(a, b)

if(solutions is None):
    print("Undetermined solution")
else:
    print(solutions)