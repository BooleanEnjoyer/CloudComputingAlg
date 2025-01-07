
from gurobipy import Model, GRB, quicksum

def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights
    model = Model("GlobalOptimization")

    