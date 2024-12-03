from Phase1 import independent_optimization

tasks = [0, 1, 2]
task_subtasks = {
    0: [0, 1],
    1: [0, 1, 2],
    2: [0, 1, 2, 3],
}

resources = [0, 1, 2, 3, 4]

exec_times = {
    (0, 0): 6, (0, 1): 5, (0, 2): 4, (0, 3): 3.5, (0, 4): 3,
    (1, 0): 5, (1, 1): 4.2, (1, 2): 3.6, (1, 3): 3, (1, 4): 2.8,
    (2, 0): 4, (2, 1): 3.5, (2, 2): 3.2, (2, 3): 2.8, (2, 4): 2.4
}

p = [1, 1.2, 1.5, 1.8, 2]

costs = {key: p[key[0]] * exec_times[key] for key in exec_times}

deadlines = {0: 50000, 1: 70000, 2: 10000}
budgets = {0: 50000, 1: 60000, 2: 700000}
tl = [1, 1, 1]
weights = (0.5, 0.5)

allocation_info, allocation_matrix, obj_value = independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl)

print("Allocation Info:")
print(allocation_info)
print("\nAllocation Matrix:")
print(allocation_matrix)
print(f"\nObjective Value: {obj_value}")