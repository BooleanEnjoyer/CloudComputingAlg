from Phase1Gekko import independent_optimization
from util import create_costs_matrix
from Phase2 import genetic_optimization
from generic import global_optimization

class Analysis:
    def __init__(self, allocation_matrix, exec_times, costs, weights):
        self.a = allocation_matrix
        self.exec_times = exec_times
        self.costs = costs
        self.wt, self.we = weights
        self.num_tasks = len(allocation_matrix)
        self.num_resources = len(allocation_matrix[0])

    def overload_penalty(self, j, a=None):
        if a == None:
            a = self.a
        return sum(a[i][j] for i in range(self.num_tasks))

    def u_local(self, i, a=None):
        if a == None:
            a = self.a
        t = max(
            min(1, a[i][j]) * self.exec_times[i + 1, j + 1] * self.overload_penalty(j, a)
            for j in range(self.num_resources)
        )
        e = sum(
            a[i][j] * self.costs[i + 1, j + 1] for j in range(self.num_resources)
        )
        u = self.wt * t + self.we * e
        return 1 / u if u > 0 else 0

    def u_global(self):
        return sum(self.u_local(i) for i in range(self.num_tasks))

    def social_justice(self, a_independent, i):
        o = self.u_local(i)
        oi = self.u_local(i, a_independent)
        return round((o - oi) / oi, 2)
    
    def social_justices(self, a_independent):
        return [self.social_justice(a_independent, i) for i in range(self.num_tasks)]
    
    def print_solution(self):
        for row in self.a:
            print(row)



class Test:
    def __init__(self, tasks, task_subtasks, resources, exec_times, deadlines, budgets, weights, tl, price_vector):
        self.tasks = tasks
        self.task_subtasks= task_subtasks
        self.resources = resources
        self.costs = create_costs_matrix(tasks, resources, price_vector, exec_times)
        self.exec_times = exec_times
        self.deadlines = deadlines
        self.budgets = budgets
        self.weights = weights
        self.tl = tl

    def run_all(self):
        allocation_info, allocation_matrix, obj_value = independent_optimization(self.tasks, self.task_subtasks, self.resources, self.costs, self.exec_times, self.deadlines, self.budgets, self.weights, self.tl)

        optimized_allocation = genetic_optimization(self.tasks, self.resources, self.exec_times, allocation_matrix)

        global_optimized = global_optimization(self.tasks, self.task_subtasks, self.resources, self.costs, self.exec_times, self.deadlines, self.budgets, self.weights, self.tl)

        independentAnalysis = Analysis(allocation_matrix, exec_times=self.exec_times, costs=self.costs, weights=self.weights)
        geneticAnalysis = Analysis(optimized_allocation, exec_times=self.exec_times, costs=self.costs, weights=self.weights)
        globalAnalysis = Analysis(global_optimized, exec_times=self.exec_times, costs=self.costs, weights=self.weights)
        return independentAnalysis, geneticAnalysis, globalAnalysis


