import numpy as np

def f(x):
    return x**3 - x - 1 #2 * np.exp(-x)#np.sin(x) - np.cos(x) + 1

def picard_iteration(f, x0, tol = np.finfo(np.float128).eps, max_iter=100):
    """
    Picard iteration: x_{n+1} = g(x_n).
    """
    x = x0
    for i in range(max_iter):
        x_new = f(x)
        if abs(x_new - x) < tol:
            print(f"Picard: Converged in {i + 1} iterations.")
            return x_new, i + 1
        x = x_new
    print("Picard: Maximum iterations reached without convergence.")
    return x, max_iter

def mann_iteration(f, x0, tol = np.finfo(np.float128).eps, max_iter=100, alpha=0.5):
    """
    Mann iteration: x_{n+1} = (1 - alpha) * x_n + alpha * g(x_n).
    """
    x = x0
    for i in range(max_iter):
        x_new = (1 - alpha) * x + alpha * f(x)
        if abs(x_new - x) < tol:
            print(f"Mann: Converged in {i + 1} iterations.")
            return x_new, i + 1
        x = x_new
    print("Mann: Maximum iterations reached without convergence.")
    return x, max_iter

def ishikawa_iteration(f, x0, tol = np.finfo(np.float128).eps, max_iter=100, alpha=0.5, beta=0.5):
    """
    Ishikawa iteration: x_{n+1} = (1 - alpha) * x_n + alpha * g((1 - beta) * x_n + beta * g(x_n)).
    """
    x = x0
    for i in range(max_iter):
        intermediate = (1 - beta) * x + beta * f(x)
        x_new = (1 - alpha) * x + alpha * f(intermediate)
        if abs(x_new - x) < tol:
            print(f"Ishikawa: Converged in {i + 1} iterations.")
            return x_new, i + 1
        x = x_new
    print("Ishikawa: Maximum iterations reached without convergence.")
    return x, max_iter

def krasnoselskij_iteration(f, x0, tol = np.finfo(np.float128).eps, max_iter=100, alpha=0.5):
    """
    Krasnoselskij iteration: x_{n+1} = alpha * g(x_n) + (1 - alpha) * x_n.
    """
    x = x0
    for i in range(max_iter):
        x_new = alpha * f(x) + (1 - alpha) * x
        if abs(x_new - x) < tol:
            print(f"Krasnoselskij: Converged in {i + 1} iterations.")
            return x_new, i + 1
        x = x_new
    print("Krasnoselskij: Maximum iterations reached without convergence.")
    return x, max_iter

if __name__ == "__main__":
    x0 = 1.0
    print("Solving the fixed-point problem for g(x)...\n")

    solution_picard, iter_picard = picard_iteration(f, x0)
    print(f"Picard Solution: {solution_picard}, Residual: {solution_picard**3 - np.exp(-solution_picard**2) + np.sin(solution_picard) - 4}\n")

    solution_mann, iter_mann = mann_iteration(f, x0, alpha=0.689)
    print(f"Mann Solution: {solution_mann}, Residual: {solution_mann**3 - np.exp(-solution_mann**2) + np.sin(solution_mann) - 4}\n")

    solution_ishikawa, iter_ishikawa = ishikawa_iteration(f, x0, alpha=0.7906, beta=0.8241)
    print(f"Ishikawa Solution: {solution_ishikawa}, Residual: {solution_ishikawa**3 - np.exp(-solution_ishikawa**2) + np.sin(solution_ishikawa) - 4}\n")

    solution_krasnoselskij, iter_krasnoselskij = krasnoselskij_iteration(f, x0, alpha=0.689)
    print(f"Krasnoselskij Solution: {solution_krasnoselskij}, Residual: {solution_krasnoselskij**3 - np.exp(-solution_krasnoselskij**2) + np.sin(solution_krasnoselskij) - 4}\n")
