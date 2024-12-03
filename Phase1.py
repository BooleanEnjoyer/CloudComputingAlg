from gurobipy import Model, GRB, quicksum


def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights  # Weights for time and cost
    model = Model("IndependentOptimization")

    b = model.addVars(tasks, task_subtasks, resources, vtype=GRB.BINARY, name="b")


    T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")

    model.setObjective(
        we * quicksum(costs[i, k] * b[i, k, j] for i in tasks for k in task_subtasks for j in resources) + wt * T_turnaround,
        GRB.MINIMIZE
    )

    # Constraints:
    for i in tasks:
        for k in task_subtasks[i]:
            model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")


        model.addConstr(quicksum(exec_times[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= deadlines[i],
            name=f"Deadline_Task_{i}"
        )

        model.addConstr(
            quicksum(costs[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= budgets[i],
            name=f"Budget_Task_{i}"
        )

    for j in resources:
        for i in tasks:
            model.addConstr(
                quicksum(b[i, k, j] for k in task_subtasks) <= 1,
                name=f"Resource_{j}_Task_{i}_Capacity"
            )

    # Turnaround time constraint (execution + communication times)
    # TODO dodać tutaj może bij???????
    model.addConstr(
        T_turnaround >= quicksum(tl) + quicksum(exec_times[i, k] for i in tasks for k in task_subtasks),
        name="TurnaroundTime"
    )

    model.optimize()


    # Display
    allocation_info = []
    allocation_matrix = []

    if model.Status == GRB.OPTIMAL:
        for i in tasks:
            task_info = f"Task {i}:"
            task_row = [0] * len(resources)
            for k in task_subtasks[i]:
                assigned_resources = []
                for idx, j in enumerate(resources):
                    if b[i, k, j].X > 0.5:
                        assigned_resources.append(j)
                        task_row[idx] = 1
                task_info += f"\n  Subtask {k} is assigned to Resources: {assigned_resources}"
            allocation_info.append(task_info)
            allocation_matrix.append(task_row)

        return "\n".join(allocation_info), allocation_matrix, model.ObjVal