from metrics import Analysis, Test
from Phase1Gekko import independent_optimization
from util import create_costs_matrix
from Phase2 import genetic_optimization
from generic import global_optimization

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

deadlines = {1: 50, 2: 70, 3: 100}
budgets = {1: 50, 2: 60, 3: 70}
weights = (0.5, 0.5)

test = Test(budgets=budgets, price_vector=price_vector, task_subtasks=task_subtasks, tasks=tasks, resources=resources, exec_times=exec_times, deadlines=deadlines, weights=weights, tl=tl)

independenti, genetici, globali = test.run_all()

independenti.print_solution()
print(independenti.u_global())
genetici.print_solution()
print(genetici.u_global())
globali.print_solution()
print(globali.u_global())

print("\nsocial justice genetic")
print(genetici.social_justices(independenti.a))
print("\nsocial justice global")
print(globali.social_justices(independenti.a))