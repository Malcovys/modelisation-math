from pulp import LpProblem, LpMaximize, LpMinimize, LpVariable, LpStatus, value, LpAffineExpression
import pandas as pd

def lp_extract_data_from_csv(
    path: str,
    objective_col: str,
    decision_var_col: str
) -> dict[str, list]:
    # Load csv data
    data_frame = pd.read_csv(path)
    data_frame_without_last_row = data_frame.iloc[:-1, :]  # Ignore the last row (ressouces row)

    # Get decision variables
    decision_vars: list[str] = data_frame_without_last_row[decision_var_col].tolist()

    # Get decision variables coefficients
    decision_vars_coef: list[float] = data_frame_without_last_row[objective_col].tolist()

    # Get resource headers (exclude decision_var_col and to_maximize)
    exclude_columns = {decision_var_col, objective_col}
    ressources_headers: list[str] = [col for col in data_frame.columns if col not in exclude_columns]

    # Get constraints coefficients (organized by resource, not by product)
    constraintes_coef: list[list[float]] = [[] for _ in range(len(ressources_headers))]
    for ressource_index, ressource_header in enumerate(ressources_headers):
        for value in data_frame_without_last_row[ressource_header]:
            constraintes_coef[ressource_index].append(float(value))

    # Get inequality constraints (last row)
    constraintes_inequality: list[float] = [
        float(value) for value in data_frame.iloc[-1, :][ressources_headers]
    ]

    return {
        "decision_vars": decision_vars,
        "decision_vars_coef": decision_vars_coef,
        "constraintes_coef": constraintes_coef,
        "constraintes_inequality": constraintes_inequality
    }


def lp_solve(
    decision_vars: list[str], 
    decision_vars_coef: list[float],
    constraintes_coef: list[list[float]],
    constraintes_inequality: list[float],
    maximize: bool,
) -> dict[str, float]:
    # Instancie the LpProblem model
    lp_prob = LpProblem("lp_problem", LpMaximize if maximize else LpMinimize)

    # Define decision variables
    decision_variables: dict[str, LpVariable] = dict()

    for i in range(len(decision_vars)):
        decision_variables.update({
            f"x{i+1}": LpVariable(decision_vars[i], lowBound=0)
        })
    # print(decision_variables)

    # Set Objective function
    objective_func = LpAffineExpression()
    for index in range(len(decision_vars)):
        objective_func += decision_vars_coef[index] * decision_variables[f"x{index+1}"]

    lp_prob += objective_func

    # Set Constraintes
    # print(constraintes_coef)
    for i in range(len(constraintes_coef)):
        constrainte = LpAffineExpression()

        for j in range(len(decision_vars)):
            constrainte += constraintes_coef[i][j] * decision_variables[f"x{j+1}"]
        
        lp_prob += constrainte <= constraintes_inequality[i]
    
    # print(lp_prob)

    # Resolve
    lp_prob.solve()
    # print(LpStatus[solve_status])

    # Set solutions
    solutions: dict[str, float] = dict()
    for name, val in decision_variables.items():
        solutions.update({val.name: value(val)})
    
    return solutions


def lp_maximize_from_csv(
    path: str,
    objective_col: str,
    decision_var_col: str
) -> dict[str, float]:
    data = lp_extract_data_from_csv(path, objective_col, decision_var_col)

    return lp_solve(
        decision_vars=data["decision_vars"],
        decision_vars_coef=data["decision_vars_coef"],
        constraintes_coef=data["constraintes_coef"],
        constraintes_inequality=data["constraintes_inequality"],
        maximize=True,
    )

def lp_minimize_from_csv(
    path: str,
    objective_col: str,
    decision_var_col: str
) -> dict[str, float]:
    data = lp_extract_data_from_csv(path, objective_col, decision_var_col)

    return lp_solve(
        decision_vars=data["decision_vars"],
        decision_vars_coef=data["decision_vars_coef"],
        constraintes_coef=data["constraintes_coef"],
        constraintes_inequality=data["constraintes_inequality"],
        maximize=False,
    )