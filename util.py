import numpy as np

def create_costs_matrix(tasks, resources, price_vector, exec_times):
    rows = len(tasks)
    cols = len(resources)
    matrix = np.zeros((rows, cols))
    for (i, j), value in exec_times.items():
        matrix[i - 1, j - 1] = value
    price_array = np.array(price_vector)
    adjusted_matrix = matrix * price_array
    costs = {
        (i + 1, j + 1): round(float(adjusted_matrix[i, j]), 2)
        for i in range(rows)
        for j in range(cols)
    }
    return costs