import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from Phase1Gekko import independent_optimization
from Phase2 import genetic_optimization
from generic import global_optimization
from Exper2data import exec_times, costs
import random


def u_global(a, exec_times, costs, weights):
    wt, we = weights
    num_tasks = len(a)
    num_resources = len(a[0])

    def overload_penalty(j):
        return sum(a[i][j] for i in range(num_tasks))

    def u_local(i):
        t = max(min(1, a[i][j]) * exec_times[i + 1, j + 1] * overload_penalty(j) for j in range(num_resources))
        e = sum(a[i][j] * costs[i + 1, j + 1] for j in range(num_resources))
        u = wt * t + we * e
        return 1/u if u > 0 else 0

    return sum(u_local(i) for i in range(num_tasks))


tasks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
resources = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
price_vector = [1.8, 1.3, 1.6, 1.8, 2.9, 2.6, 2.3, 2.3, 1.5, 2.7]

weights = (0.5, 0.5)
deadlines = {1: 100000000, 2: 100000000, 3: 100000000, 4: 100000000, 5: 100000000, 6: 100000000, 7: 100000000, 8: 100000000, 9: 100000000, 10: 100000000}
budgets = {1: 100000000, 2: 100000000, 3: 100000000, 4: 100000000, 5: 100000000, 6: 100000000, 7: 100000000, 8: 100000000, 9: 100000000, 10: 100000000}


num_tasks_range = range(1, 11)
genetic_utilities = []
global_utilities = []


def experiment_iteration(num_tasks):
    tasks = list(range(1, num_tasks + 1))

    task_subtasks = {task: [1, 2, 3] for task in tasks}
    tl = [1, 2, 3]

    # Independent Optimization (Phase 1)
    allocation_info, allocation_matrix, _ = independent_optimization(
        tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl
    )

    # Genetic Optimization (Phase 2)
    optimized_allocation = genetic_optimization(tasks, resources, exec_times, allocation_matrix)

    # Global Optimization (Phase 3)
    global_optimized = global_optimization(
        tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl
    )

    # Calculate Utilities
    genetic_util = u_global(optimized_allocation, exec_times, costs, weights)
    global_util = u_global(global_optimized, exec_times, costs, weights)
    print("\n genetically optimized allocation Matrix")
    print(f"\n{optimized_allocation}")
    print(f"\nObjective Value genetic: {genetic_util}")

    print("\n Globally optimized allocation Matrix")
    print(f"\n{optimized_allocation}")
    print(f"\nObjective Value global: {global_util}")

    return genetic_util, global_util


with ThreadPoolExecutor() as executor:
    results = list(executor.map(experiment_iteration, num_tasks_range))

# Extract Results
genetic_utilities, global_utilities = zip(*results)


# Plot Results
plt.figure(figsize=(10, 6))
plt.plot(num_tasks_range, genetic_utilities, label='Genetic Optimization Utility', marker='o')
plt.plot(num_tasks_range, global_utilities, label='Global Optimization Utility', marker='x')
plt.title('Utility vs. Number of Tasks')
plt.xlabel('Number of Tasks')
plt.ylabel('Utility')
plt.legend()
plt.grid()
plt.savefig('utility_vs_tasks.png')  # Save the plot
plt.show()
