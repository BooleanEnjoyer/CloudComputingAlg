from gurobipy import Model, GRB, quicksum


def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights
    model = Model("IndependentOptimization")

    all_allocation_info = []
    all_allocation_matrix = []
    all_obj_values = []

    for task_index in tasks:
        # Constraint 7 constraint because it is binary
        b = model.addVars(task_subtasks[task_index], resources, vtype=GRB.BINARY, name="b")

        T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")

        model.setObjective(
            we * quicksum(costs[task_index, j] * b[i, j] for i in task_subtasks[task_index] for j in resources) + wt * T_turnaround,
            GRB.MINIMIZE
        )

        # Constraint 8
        model.addConstr(T_turnaround <= deadlines[task_index],
            name=f"Deadline_Task_{task_index}"
        )

        # Constraint 9
        model.addConstr(
            quicksum(costs[task_index, j] * b[i, j] for i in task_subtasks[task_index] for j in resources) <= budgets[task_index],
            name=f"Budget_Task_{task_index}"
        )

        # Constraint 10
        for i in task_subtasks[task_index]:
            model.addConstr(quicksum(b[i, j] for j in resources) == 1, name=f"Subtask_{task_index}_{i}_Assignment")

        # Constraint 11
        for j in resources:
                model.addConstr(quicksum(b[i, j] for i in task_subtasks[task_index]) <= 1, name=f"Resource_{j}_Task_{task_index}_Capacity")

        # Constraint 12 (simplified max)
        model.addConstr(
            T_turnaround >= quicksum(tl) + quicksum(exec_times[task_index, j] * b[k, j] for k in task_subtasks[task_index] for j in resources),
            name="TurnaroundTime"
        )

        model.optimize()

        allocation_info = []
        allocation_matrix = []

        if model.Status == GRB.OPTIMAL:
            task_info = f"Task {task_index}:"
            task_row = [0] * len(resources)
            for i in task_subtasks[task_index]:
                assigned_resources = []
                for idx, j in enumerate(resources):
                    if b[i, j].X > 0.5:
                        assigned_resources.append(j)
                        task_row[idx] = 1
                task_info += f"\n  Subtask {i} is assigned to Resources: {assigned_resources}"
            allocation_info.append(task_info)
            allocation_matrix.append(task_row)

            all_allocation_info.append("\n".join(allocation_info))
            all_allocation_matrix.append(task_row)
            all_obj_values.append(model.ObjVal)
        elif model.Status == GRB.INFEASIBLE:
            print(f"Task {task_index}: Model is infeasible. Relaxing constraints to diagnose issues.")
            model.computeIIS()
            model.write(f"task_{task_index}_model.ilp")
        else:
            print(f"Task {task_index}: Optimization failed.")

    return all_allocation_info, all_allocation_matrix, all_obj_values
