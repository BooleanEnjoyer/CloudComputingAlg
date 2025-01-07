from Phase1Gekko import independent_optimization
from util import create_costs_matrix
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

def u_global(a, exec_times, costs, weights):
    wt, we = weights
    num_tasks = len(allocation_matrix)
    num_resources = len(allocation_matrix[0])

    def overload_penalty(j):
        return sum(a[i][j] for i in range(num_tasks))

    def u_local(i):
        t = max(min(1, a[i][j]) * exec_times[i + 1, j + 1] * overload_penalty(j) for j in range(num_resources))
        e = sum(a[i][j] * costs[i + 1, j + 1] for j in range(num_resources))
        u = wt * t + we * e
        return 1/u if u > 0 else 0

    return sum(u_local(i) for i in range(num_tasks))

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

global_optimized = global_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl)

print("Allocation Info for All Tasks:\n")
for task_info in allocation_info:
    print(task_info)
    print("-" * 40)


print("\nAllocation Matrix for All Tasks:")
for row in allocation_matrix:
    print(row)
print(f"\nObjective Value independent: {u_global(allocation_matrix, exec_times, costs, weights)}")

print("\n genetically optimized allocation Matrix")
for row in optimized_allocation:
    print(row)
print(f"\nObjective Value genetic: {u_global(optimized_allocation, exec_times, costs, weights)}")

for row in global_optimized:
    print(row)

print(f"\nObjective Value global: {u_global(global_optimized, exec_times, costs, weights)}")