from Phase1 import independent_optimization


# tasks = [1, 2, 3]
# subtasks = [2, 3, 4]
# price_vector = [1, 1.2, 1.5, 1.8, 2]
# resources = [1, 2, 3, 4, 5]
#
# exec_times = {
#     (1, 1): 6, (1, 2): 5, (1, 3): 4, (1, 4): 3.5, (1, 5): 3,
#     (2, 1): 5, (2, 2): 4.2, (2, 3): 3.6, (2, 4): 3, (2, 5): 2.8,
#     (3, 1): 4, (3, 2): 3.5, (3, 3): 3.2, (3, 4): 2.8, (3, 5): 2.4
# }
#
# costs = {key: round(key[0] * exec_times[key], 1) for key in exec_times}
#
# print(exec_times)
# print(costs)
#
# tl = [2, 4, 5]
#
# deadlines = {1: 20, 2: 50, 3: 700}
# budgets = {1: 25, 2: 30, 3: 40}



tasks = [1, 2, 3]
# subtasks = [1, 2, 3]
task_subtasks = {
    1: [1],          # Task 1 has 1 subtask
    2: [1, 2],       # Task 2 has 2 subtasks
    3: [1, 2, 3],    # Task 3 has 3 subtasks
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
tl = [1, 2, 3]  # Communication times
weights = (0.5, 0.5)

allocation_info, allocation_matrix, obj_value = independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl)

print("Allocation Info:")
print(allocation_info)
print("\nAllocation Matrix:")
print(allocation_matrix)
print(f"\nObjective Value: {obj_value}")


# print("Allocation Matrix:", allocation)
# print("Objective Value:", obj_value)



# Phase 1
# allocation, T_turnaround = independent_optimization(tasks, subtasks, resources, costs, exec_times, deadlines, budgets, tl)
# print("Initial Allocation:", allocation)
# print("Turnaround:", T_turnaround)








# allocation_matrix, T_turnaround = independent_optimization(tasks, subtasks, resources, costs, exec_times, deadlines, budgets, tl)
#
# print("Task-Resource Allocation Matrix:")
# for row in allocation_matrix:
#     print(row)
# print("Turnaround Time:", T_turnaround)