from Phase1 import independent_optimization
from util import create_costs_matrix

tasks = [1, 2, 3]
resources = [1, 2, 3, 4, 5]
price_vector = [1, 1.2, 1.5, 1.8, 2]

# SCENARIO 2 (similar to paper one)
exec_times = {
    (1, 1): 6, (1, 2): 5, (1, 3): 4, (1, 4): 3.5, (1, 5): 3,
    (2, 1): 5, (2, 2): 4.2, (2, 3): 3.6, (2, 4): 3, (2, 5): 2.8,
    (3, 1): 4, (3, 2): 3.5, (3, 3): 3.2, (3, 4): 2.8, (3, 5): 2.4
}
task_subtasks = {
    1: [1, 2],
    2: [1, 2, 3],
    3: [1, 2, 3, 4]
}
tl = [1, 2, 3, 4]


costs = create_costs_matrix(tasks, resources, price_vector, exec_times)
print(costs)

deadlines = {1: 50, 2: 70, 3: 100}
budgets = {1: 50, 2: 60, 3: 70}
weights = (0.5, 0.5)

allocation_info, allocation_matrix, obj_value = independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl)

print("Allocation Info:")
print(allocation_info)
print("\nAllocation Matrix:")
print(allocation_matrix)
print(f"\nObjective Value: {obj_value}")







# ADJUST PROPERLY EXEC AND SUBTASKS!!!
# tl dont have to be number also like amount of tasks technically


# SCENARIO 1
# resources = [1, 2, 3]

# exec_times = {
#     (1, 1): 6, (1, 2): 5, (1, 3): 4,
#     (2, 1): 5, (2, 2): 4.2, (2, 3): 3.6,
#     (3, 1): 4, (3, 2): 3.5, (3, 3): 3.2
# }
# task_subtasks = {
#     1: [1],
#     2: [1, 2],
#     3: [1, 2, 3],
# }
# tl = [1, 2, 3]
