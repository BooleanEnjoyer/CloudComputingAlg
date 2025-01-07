from Phase1Gekko import independent_optimization
from util import create_costs_matrix, u_global
from Phase2 import genetic_optimization
from generic import global_optimization

# tl dont have to be number also like amount of tasks technically


# SCENARIO 1
# tasks = [1, 2, 3]
# resources = [1, 2, 3]
# price_vector = [1, 1.2, 1.5]
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


# SCENARIO 2 (similar to paper one)
tasks = [1, 2, 3]
price_vector = [1, 1.2, 1.5, 1.8, 2]
resources = [1, 2, 3, 4, 5]
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

optimized_allocation = genetic_optimization(tasks, resources, exec_times, allocation_matrix)

print("Allocation Info for All Tasks:\n")
for task_info in allocation_info:
    print(task_info)
    print("-" * 40)


print("\nAllocation Matrix for All Tasks:")
for row in allocation_matrix:
    print(row)
print(f"\nObjective Value: {obj_value}")

print("\n genetically optimized allocation Matrix")
for row in optimized_allocation:
    print(row)

global_optimized = global_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl)
for row in global_optimized:
    print(row)


print("Utilities:")
# print(f"Genetic: {calculate_utilization(optimized_allocation, exec_times, costs, weights)}")
# print(f"Global: {calculate_utilization(global_optimized, exec_times, costs, weights)}")


# print(f"Genetic util: {u(optimized_allocation, exec_times, costs, weights, resources, tasks)}")
# print(f"Global util: {u(global_optimized, exec_times, costs, weights, resources, tasks)}")



print(f"Genetic util 2: {u_global(optimized_allocation, exec_times, costs, weights)}")
print(f"Global util 2: {u_global(global_optimized, exec_times, costs, weights)}")