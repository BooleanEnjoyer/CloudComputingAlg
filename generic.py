
from gekko import GEKKO

def global_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights
    m = GEKKO(remote=False)
    def sum(l):
        return m.sum(list(l))

    a = {}

    for i in tasks:
        for j in resources:
            a[i,j] = m.Var(value=0, lb=0, integer=True, name=f"a_{i}_{j}")
    
    def overload_penalty(j):
        return sum(a[i,j] for i in tasks)

    def task_time(i):
        t = 0
        for j in resources:
            t = m.max3(t, m.max3(1, a[i,j]) * exec_times[i,j] * overload_penalty(j))
        return t

    def u(i):
        t = task_time(i)
        e = sum(a[i, j] * costs[i, j] for j in resources)
        return wt * t + we * e

    m.Obj(sum(u(i) for i in tasks))

    # all subtasks are being done constraint
    for i in tasks:
        m.Equation(sum(a[i,j] for j in resources) == len(task_subtasks[i]))
    
    # budget constraint
    for i in tasks:
        sum(a[i, j] * costs[i, j] for j in resources) <= budgets[i]

    # deadline constraint
    for i in tasks:
        task_time(i) <= deadlines[i]

    m.solve()

    res = []
    for i in tasks:
        row = []
        for j in resources:
            row.append(a[i,j].value[0])
        res.append(row)
    
    return res


