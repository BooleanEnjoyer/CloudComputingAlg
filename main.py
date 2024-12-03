from Phase1 import independent_optimization

tasks = [1, 2, 3]
task_subtasks = {
    1: [1],
    2: [1, 2],
    3: [1, 2, 3],
}

resources = [1, 2, 3, 4, 5]

exec_times = {
    (1, 1): 6, (1, 2): 5, (1, 3): 4,
    (2, 1): 5, (2, 2): 4.2, (2, 3): 3.6,
    (3, 1): 4, (3, 2): 3.5, (3, 3): 3.2
}
costs = {key: key[0] * exec_times[key] for key in exec_times}

deadlines = {1: 50, 2: 70, 3: 100}
budgets = {1: 50, 2: 60, 3: 70}
tl = [1, 2, 3]
weights = (0.5, 0.5)

allocation_info, allocation_matrix, obj_value = independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl)

print("Allocation Info:")
print(allocation_info)
print("\nAllocation Matrix:")
print(allocation_matrix)
print(f"\nObjective Value: {obj_value}")