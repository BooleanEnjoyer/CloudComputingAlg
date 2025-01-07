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
