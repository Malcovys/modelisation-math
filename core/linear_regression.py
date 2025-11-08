import numpy as np

def linear_regression_compute(
    explicative_vars: list[float],
    tagert_vars: list[float]
) -> dict[str, float]:
    # Format data to numpy array
    X = np.array(explicative_vars)
    Y = np.array(tagert_vars)

    if X.size != Y.size:
        raise ValueError("X and Y  must hanve the same size.")

    # Calculate averages
    average_X = np.average(X)
    average_Y = np.average(Y)

    # Calculate covariance of X and Y
    covariance_X_Y = np.sum((X - average_X) * (Y - average_Y))

    # Calculate variance of X
    variance_X = np.sum((X - average_X)**2)

    if variance_X == 0:
        raise ValueError("Variance of X is zero → cannot compute regression.")

    # Compute a and b
    a = covariance_X_Y / variance_X
    b = average_Y - a * average_X

    # Calculate correlation
    variance_Y = np.sum((Y - average_Y)**2)
    correlation = covariance_X_Y / np.sqrt(variance_Y * variance_X)

    return {
        "a": float(a),
        "b": float(b),
        "correlation": float(correlation)
    }


    