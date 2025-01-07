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


# def calculate_utilization(allocation_matrix, exec_times, costs, weights):
#     wt, we = weights
#     num_tasks = len(allocation_matrix)
#     num_resources = len(allocation_matrix[0])
#     total_utility = 0
#
#     for i in range(num_tasks):
#         turnaround_time = 0
#         total_cost = 0
#
#         for j in range(num_resources):
#             num_subtasks = allocation_matrix[i][j]
#             if num_subtasks > 0:
#                 execution_time = exec_times[(i + 1, j + 1)] * num_subtasks
#                 cost = costs[(i + 1, j + 1)] * num_subtasks
#
#                 turnaround_time = max(turnaround_time, execution_time)
#                 total_cost += cost
#
#         task_utility = 1 / (wt * turnaround_time + we * total_cost) if turnaround_time + total_cost > 0 else 0
#         total_utility += task_utility
#
#     return total_utility
#
#
# def task_time(a, exec_times, resources, tasks, i):
#     t = 0
#     for j in resources:
#         t = max(t, a[i][j] * exec_times[i, j] * overload_penalty(a, j, tasks))
#     return t
#
#
# def overload_penalty(a, j, tasks):
#     return sum(a[i][j] for i in tasks)


# def u(a, exec_times, costs, weights, resources, tasks):
#     wt, we = weights
#     sum_utils = 0
#     for i in tasks:
#         t = task_time(a, exec_times, resources, tasks, i)
#         e = sum(a[i][j] * costs[i, j] for j in resources)
#         temp_util = wt * t + we * e
#         if temp_util > 0:
#             sum_utils += 1 / temp_util
#     return sum_utils


def u_global(a, exec_times, costs, weights):
    wt, we = weights
    num_tasks = len(a)  # Number of tasks (rows in the matrix)
    num_resources = len(a[0])  # Number of resources (columns in the matrix)

    def overload_penalty(j):
        return sum(a[i][j] for i in range(num_tasks))

    def u_local(i):
        t = max(min(1, a[i][j]) * exec_times[i + 1, j + 1] * overload_penalty(j) for j in range(num_resources))
        e = sum(a[i][j] * costs[i + 1, j + 1] for j in range(num_resources))
        u = wt * t + we * e
        return 1 / u if u > 0 else 0

    return sum(u_local(i) for i in range(num_tasks))



# Metody temp
# resources2 = list(range(1, 101))  # Generate numbers from 1 to 100
# formatted_resources = f"resources = {resources2}"  # Format as a string
#
# # Display the structure in the terminal
# print(formatted_resources)
#


# def generate_price_vector(size, min_value=1, max_value=3, precision=1):
#     # Generate random values with specified precision
#     price_vector = [round(random.uniform(min_value, max_value), precision) for _ in range(size)]
#     # Format and display the structure
#     formatted_vector = f"price_vector = {price_vector}"
#     print(formatted_vector)



# def generate_exec_times(num_rows, num_columns, min_value=2, max_value=6, precision=1):
#     exec_times = {}
#     for row in range(1, num_rows + 1):  # Iterate through rows
#         for col in range(1, num_columns + 1):  # Iterate through columns
#             # Generate a random value with specified precision
#             exec_times[(row, col)] = round(random.uniform(min_value, max_value), precision)
#
#     # Format and display the structure
#     formatted_exec_times = "exec_times = {\n"
#     for (row, col), value in exec_times.items():
#         formatted_exec_times += f"    ({row}, {col}): {value},\n"
#     formatted_exec_times = formatted_exec_times.rstrip(",\n") + "\n}"  # Clean up trailing comma and newline
#     return formatted_exec_times
#
#
# # Example usage
# format = generate_exec_times(3, 100)
# # Generate exec_times with 3 rows and 100 columns



# def display_costs_matrix_as_dict(costs):
#     formatted_costs = "costs = {\n"
#     for (i, j), value in costs.items():
#         formatted_costs += f"    ({i}, {j}): {value},\n"
#     formatted_costs = formatted_costs.rstrip(",\n") + "\n}"  # Remove trailing comma and newline
#     print(formatted_costs)
#
# display_costs_matrix_as_dict(costs)