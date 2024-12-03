# TODO working with simplified subtask assign
def independent_optimization(tasks, subtasks, resources, costs, exec_times, deadlines, budgets, tl):
    model = Model("IndependentOptimization")

    # Variables: bij = 1 if task i is assigned to resource j
    b = model.addVars(tasks, resources, vtype=GRB.BINARY, name="b")

    # Total execution times for each task
    total_exec_times = {
        i: sum(exec_times[i, k] for k in subtasks) for i in tasks
    }

    # Total costs for each task
    total_costs = {
        i: sum(costs[i, k] for k in subtasks) for i in tasks
    }

    # Total execution time variable
    T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")

    # Objective: Minimize weighted sum of cost and execution time
    obj = 0.5 * (quicksum(total_costs[i] * b[i, j] for i in tasks for j in resources) +
                 quicksum(total_exec_times[i] * b[i, j] for i in tasks for j in resources)) + 0.5 * T_turnaround
    model.setObjective(obj, GRB.MINIMIZE)

    # Constraints
    for i in tasks:
        # Each task should be assigned to exactly one resource
        model.addConstr(quicksum(b[i, j] for j in resources) == 1, name=f"Task_{i}_Assignment")

    for j in resources:
        # Resource capacity constraint (each resource can handle at most one task at a time)
        model.addConstr(quicksum(b[i, j] for i in tasks) <= 1, name=f"Resource_{j}_Capacity")

    for i in tasks:
        # Deadline and budget constraints
        model.addConstr(total_exec_times[i] * quicksum(b[i, j] for j in resources) <= deadlines[i],
                        name=f"Task_{i}_Deadline")
        model.addConstr(total_costs[i] * quicksum(b[i, j] for j in resources) <= budgets[i], name=f"Task_{i}_Budget")

    # Turnaround time constraints: Sum of execution time + communication time
    model.addConstr(T_turnaround >= quicksum(tl) + quicksum(total_exec_times[i] for i in tasks), name="TurnaroundTime")

    # Optimize
    model.optimize()

    if model.Status == GRB.OPTIMAL:
        allocation = {i: j for i in tasks for j in resources if b[i, j].X > 0.5}
        return allocation, T_turnaround.X
    elif model.Status == GRB.INFEASIBLE:
        print("Model is infeasible. Relaxing constraints to diagnose issues.")
        model.computeIIS()  # Identify infeasible subset
        model.write("model.ilp")  # Save the IIS for inspection
        return None, None
    else:
        print("Optimization problem not solved.")
        return None, None