
from gekko import GEKKO
better = [
[0, 0, 1, 0, 1],
[0, 0, 1, 1, 1],
[1, 2, 0, 1, 0]]

def global_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights
    m = GEKKO(remote=False)
    m.options.SOLVER = 3
    m.options.IMODE = 3
    m.solver_options = ['max_iter 500',  # Increase maximum iterations
                    'tol 1e-8',     # Adjust tolerance
                    'minlp_maximum_iterations 1000', \
                    # minlp iterations with integer solution
                    'minlp_max_iter_with_int_sol 300', \
                    # treat minlp as nlp
                    'minlp_as_nlp 0', \
                    # nlp sub-problem max iterations
                    'nlp_maximum_iterations 500', \
                    # 1 = depth first, 2 = breadth first
                    'minlp_branch_method 1', \
                    # maximum deviation from whole number
                    'minlp_integer_tol 0.005', \
                    # covergence tolerance
                    'minlp_gap_tol 0.00001'
    ]

    def sum(l):
        return m.sum(list(l))

    a = {}
    for i in tasks:
        for j in resources:
            a[i,j] = m.Var(value=0, lb=0, integer=True, name=f"a_{i}_{j}")
    
    T_turnaround = {}
    for i in tasks:
        T_turnaround[i] = m.Var(value=0, name=f"T_turnaround_{i}")
    
    
    def overload_penalty(j):
        return sum(a[i,j] for i in tasks)

    # def task_time(i):
    #     t = 0
    #     for j in resources:
    #         t = m.max3(t, m.min3(1, a[i,j]) * exec_times[i,j] * overload_penalty(j))
    #     return t

    def u(i):
        t = T_turnaround[i]
        e = sum(a[i, j] * costs[i, j] for j in resources)
        return wt * t + we * e

    m.Obj(sum(u(i) for i in tasks))

    for i in tasks:
        for j in resources:
            m.Equation(T_turnaround[i] >= a[i, j] * exec_times[i,j] * overload_penalty(i, j))

    # all subtasks are being done constraint

    for i in tasks:
        m.Equation(sum(a[i,j] for j in resources) == len(task_subtasks[i]))
    

    for i in tasks:
        m.Equation(sum(a[i, j] * costs[i, j] for j in resources) <= budgets[i])

   
    for i in tasks:
        m.Equation(T_turnaround[i] <= deadlines[i])

    m.solve()

    res = []
    for i in tasks:
        row = []
        for j in resources:
            row.append(int(a[i,j].value[0]))
        res.append(row)
    
    return res


