from gurobipy import Model, GRB, quicksum


def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights  # Weights for time and cost
    model = Model("IndependentOptimization")

    # Constraint 7 constraint because it is binary
    b = model.addVars(tasks, task_subtasks, resources, vtype=GRB.BINARY, name="b")

    T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")

    model.setObjective(
        we * quicksum(costs[i, k] * b[i, k, j] for i in tasks for k in task_subtasks for j in resources) + wt * T_turnaround,
        GRB.MINIMIZE
    )

    for i in tasks:
        # Constraint 8
        model.addConstr(T_turnaround <= deadlines[i],
            name=f"Deadline_Task_{i}"
        )

        # Constraint 9
        model.addConstr(
            quicksum(costs[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= budgets[i],
            name=f"Budget_Task_{i}"
        )

        # # Constraint 10
        # for k in task_subtasks[i]:
        #     model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")

    print(f"Shape of b (tasks x subtasks x resources):")
    print(f"Tasks: {len(tasks)}")
    print(f"Subtasks: {max(len(task_subtasks[i]) for i in tasks)}")  # Max number of subtasks across all tasks
    print(f"Resources: {len(resources)}")
    for i in tasks:
        for k in task_subtasks[i]:
            for j in resources:
                print(i, k, j)
                print("Bikj")
                print(b[i, k, j])
            # Skip if the (i, k) combination doesn't exist in exec_times
            # if (i, k) in exec_times:
            #     model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")
            # else:
            #     print(f"Skipping missing subtask (i={i}, k={k})")


    # Constraint 11
    for j in resources:
        for i in tasks:
            model.addConstr(
                quicksum(b[i, k, j] for k in task_subtasks[i]) <= 1,
                name=f"Resource_{j}_Task_{i}_Capacity"
            )

    # Constraint 12 (simplified max)
    model.addConstr(
        T_turnaround >= quicksum(tl) + quicksum(exec_times[i, k] * b[i, k, j] for i in tasks for k in task_subtasks for j in resources),
        name="TurnaroundTime"
    )

    model.optimize()

    # Display section
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
    elif model.Status == GRB.INFEASIBLE:
        print("Model is infeasible. Relaxing constraints to diagnose issues.")
        model.computeIIS()
        model.write("model.ilp")
        return None, None
    else:
        print("Optimization failed")
        return None, None