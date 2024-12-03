from gurobipy import Model, GRB, quicksum


def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights  # Weights for time and cost
    model = Model("IndependentOptimization")

    # Variables: b[i, k, j] = 1 if subtask k of task i is assigned to resource j
    b = model.addVars(tasks, task_subtasks, resources, vtype=GRB.BINARY, name="b")

    # Total execution time and costs
    total_exec_times = {
        i: sum(exec_times[i, k] for k in task_subtasks) for i in tasks
    }
    total_costs = {
        i: sum(costs[i, k] for k in task_subtasks) for i in tasks
    }

    # Total execution time variable (T_turnaround)
    T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")

    # Objective: Minimize weighted sum of cost and execution time
    model.setObjective(
        we * quicksum(costs[i, k] * b[i, k, j] for i in tasks for k in task_subtasks for j in resources) +
        wt * T_turnaround,
        GRB.MINIMIZE
    )

    # Constraints:
    for i in tasks:
        for k in task_subtasks[i]:  # Only iterate over the correct subtasks for each task
            # Each subtask must be assigned to exactly one resource
            model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")

        # Deadline constraint
        model.addConstr(
            quicksum(exec_times[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= deadlines[i],
            name=f"Deadline_Task_{i}"
        )
        # Budget constraint
        model.addConstr(
            quicksum(costs[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= budgets[i],
            name=f"Budget_Task_{i}"
        )

    # Resource capacity constraint
    for j in resources:
        for i in tasks:
            model.addConstr(
                quicksum(b[i, k, j] for k in task_subtasks) <= 1,
                name=f"Resource_{j}_Task_{i}_Capacity"
            )

    # Turnaround time constraint (execution + communication times)
    model.addConstr(
        T_turnaround >= quicksum(tl) + quicksum(exec_times[i, k] for i in tasks for k in task_subtasks),
        name="TurnaroundTime"
    )

    # Optimize the model
    model.optimize()

    allocation_info = []
    allocation_matrix = []

    if model.Status == GRB.OPTIMAL:
        for i in tasks:
            task_info = f"Task {i}:"
            task_row = [0] * len(resources)  # Initialize task_row with zeros (1 for each resource)
            for k in task_subtasks[i]:
                assigned_resources = []
                for idx, j in enumerate(resources):
                    if b[i, k, j].X > 0.5:  # Check if the subtask is assigned to this resource
                        assigned_resources.append(j)
                        task_row[idx] = 1  # Set the corresponding resource column to 1 for this task and subtask
                task_info += f"\n  Subtask {k} is assigned to Resources: {assigned_resources}"
            allocation_info.append(task_info)
            allocation_matrix.append(task_row)

        return "\n".join(allocation_info), allocation_matrix, model.ObjVal








# Working
# def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
#     wt, we = weights  # Weights for time and cost
#     model = Model("IndependentOptimization")
#
#     # Variables: b[i, k, j] = 1 if subtask k of task i is assigned to resource j
#     b = model.addVars(tasks, task_subtasks, resources, vtype=GRB.BINARY, name="b")
#
#     # Total execution time and costs
#     total_exec_times = {
#         i: sum(exec_times[i, k] for k in task_subtasks) for i in tasks
#     }
#     total_costs = {
#         i: sum(costs[i, k] for k in task_subtasks) for i in tasks
#     }
#
#     # Total execution time variable (T_turnaround)
#     T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")
#
#     # Objective: Minimize weighted sum of cost and execution time
#     model.setObjective(
#         we * quicksum(costs[i, k] * b[i, k, j] for i in tasks for k in task_subtasks for j in resources) +
#         wt * T_turnaround,
#         GRB.MINIMIZE
#     )
#
#     # Constraints:
#     for i in tasks:
#         for k in task_subtasks[i]:  # Only iterate over the correct subtasks for each task
#             # Each subtask must be assigned to exactly one resource
#             model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")
#
#         # Deadline constraint
#         model.addConstr(
#             quicksum(exec_times[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= deadlines[i],
#             name=f"Deadline_Task_{i}"
#         )
#         # Budget constraint
#         model.addConstr(
#             quicksum(costs[i, k] * b[i, k, j] for k in task_subtasks for j in resources) <= budgets[i],
#             name=f"Budget_Task_{i}"
#         )
#
#     # Resource capacity constraint
#     for j in resources:
#         for i in tasks:
#             model.addConstr(
#                 quicksum(b[i, k, j] for k in task_subtasks) <= 1,
#                 name=f"Resource_{j}_Task_{i}_Capacity"
#             )
#
#     # Turnaround time constraint (execution + communication times)
#     model.addConstr(
#         T_turnaround >= quicksum(tl) + quicksum(exec_times[i, k] for i in tasks for k in task_subtasks),
#         name="TurnaroundTime"
#     )
#
#     # Optimize the model
#     model.optimize()
#
#     # Create a human-readable output
#     allocation_info = []
#
#     if model.Status == GRB.OPTIMAL:
#         for i in tasks:
#             task_info = f"Task {i}:"
#             for k in task_subtasks[i]:  # Iterate through the correct subtasks for each task
#                 assigned_resources = []
#                 for j in resources:
#                     if b[i, k, j].X > 0.5:  # Check if the subtask is assigned to this resource
#                         assigned_resources.append(j)
#                 task_info += f"\n  Subtask {k} is assigned to Resources: {assigned_resources}"
#             allocation_info.append(task_info)
#
#         return "\n".join(allocation_info), model.ObjVal
#     elif model.Status == GRB.INFEASIBLE:
#         print("Model is infeasible. Relaxing constraints to diagnose issues.")
#         model.computeIIS()  # Identify infeasible subset
#         model.write("model.ilp")  # Save the IIS for inspection
#         return None, None
#     else:
#         print("Optimization failed")
#         return None, None














# # TODO ALMOST!
# def independent_optimization(tasks, subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
#     wt, we = weights  # Weights for time and cost
#     model = Model("IndependentOptimization")
#
#     # Variables: b[i, k, j] = 1 if subtask k of task i is assigned to resource j
#     b = model.addVars(tasks, subtasks, resources, vtype=GRB.BINARY, name="b")
#
#     # Total execution time and costs
#     total_exec_times = {
#         i: sum(exec_times[i, k] for k in subtasks) for i in tasks
#     }
#     total_costs = {
#         i: sum(costs[i, k] for k in subtasks) for i in tasks
#     }
#
#     # Total execution time variable (T_turnaround)
#     T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")
#
#     # Objective: Minimize weighted sum of cost and execution time
#     model.setObjective(
#         we * quicksum(costs[i, k] * b[i, k, j] for i in tasks for k in subtasks for j in resources) +
#         wt * T_turnaround,
#         GRB.MINIMIZE
#     )
#
#     # Constraints:
#     for i in tasks:
#         for k in subtasks:
#             # Each subtask must be assigned to exactly one resource
#             model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")
#
#         # Deadline constraint
#         model.addConstr(
#             quicksum(exec_times[i, k] * b[i, k, j] for k in subtasks for j in resources) <= deadlines[i],
#             name=f"Deadline_Task_{i}"
#         )
#         # Budget constraint
#         model.addConstr(
#             quicksum(costs[i, k] * b[i, k, j] for k in subtasks for j in resources) <= budgets[i],
#             name=f"Budget_Task_{i}"
#         )
#
#     # Resource capacity constraint
#     # for j in resources:
#     #     model.addConstr(
#     #         quicksum(b[i, k, j] for i in tasks for k in subtasks) <= 1,
#     #         name=f"Resource_{j}_Capacity"
#     #     )
#     for j in resources:
#         for i in tasks:
#             model.addConstr(
#                 quicksum(b[i, k, j] for k in subtasks) <= 1,
#                 name=f"Resource_{j}_Task_{i}_Capacity"
#             )
#
#
#     # Turnaround time constraint (execution + communication times)
#     model.addConstr(
#         T_turnaround >= quicksum(tl) + quicksum(exec_times[i, k] for i in tasks for k in subtasks),
#         name="TurnaroundTime"
#     )
#
#     # Optimize the model
#     model.optimize()
#
#     # Create allocation matrix
#     allocation_matrix = []
#     if model.Status == GRB.OPTIMAL:
#         for i in tasks:
#             row = []
#             for j in resources:
#                 # Check if any subtask of task i is assigned to resource j
#                 if any(b[i, k, j].X > 0.5 for k in subtasks):
#                     row.append(1)
#                 else:
#                     row.append(0)
#             allocation_matrix.append(row)
#
#         return allocation_matrix, model.ObjVal
#     elif model.Status == GRB.INFEASIBLE:
#         print("Model is infeasible. Relaxing constraints to diagnose issues.")
#         model.computeIIS()  # Identify infeasible subset
#         model.write("model.ilp")  # Save the IIS for inspection
#         return None, None
#     else:
#         print("Optimization failed")
#         return None, None













# def independent_optimization(tasks, subtasks, resources, costs, exec_times, deadlines, budgets, tl):
#     model = Model("IndependentOptimization")
#
#     # Variables: b[i, k, j] = 1 if subtask k of task i is assigned to resource j
#     b = model.addVars(tasks, subtasks, resources, vtype=GRB.BINARY, name="b")
#
#     # Total execution times for each task (sum of all subtasks' times)
#     total_exec_times = {
#         i: sum(exec_times[i, k] for k in subtasks) for i in tasks
#     }
#
#     # Total costs for each task (sum of all subtasks' costs)
#     total_costs = {
#         i: sum(costs[i, k] for k in subtasks) for i in tasks
#     }
#
#     # Total execution time variable
#     T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")
#
#     # Objective: Minimize weighted sum of cost and execution time
#     obj = 0.5 * (quicksum(total_costs[i] * b[i, k, j] for i in tasks for k in subtasks for j in resources) +
#                  quicksum(total_exec_times[i] * b[i, k, j] for i in tasks for k in subtasks for j in resources)) + 0.5 * T_turnaround
#     model.setObjective(obj, GRB.MINIMIZE)
#
#     # Constraints
#     for i in tasks:
#         for k in subtasks:
#             # Each subtask k of task i should be assigned to exactly one resource
#             model.addConstr(quicksum(b[i, k, j] for j in resources) == 1, name=f"Subtask_{i}_{k}_Assignment")
#
#     for j in resources:
#         # Resource capacity constraint: each resource can handle at most one subtask at a time
#         model.addConstr(quicksum(b[i, k, j] for i in tasks for k in subtasks) <= 1, name=f"Resource_{j}_Capacity")
#
#     for i in tasks:
#         # Deadline and budget constraints (relaxed)
#         model.addConstr(total_exec_times[i] * quicksum(b[i, k, j] for k in subtasks for j in resources) <= deadlines[i],
#                         name=f"Task_{i}_Deadline")
#         model.addConstr(total_costs[i] * quicksum(b[i, k, j] for k in subtasks for j in resources) <= budgets[i], name=f"Task_{i}_Budget")
#
#     # Turnaround time constraints: Sum of execution time + communication time
#     model.addConstr(T_turnaround >= quicksum(tl) + quicksum(total_exec_times[i] for i in tasks), name="TurnaroundTime")
#
#     # Optimize the model
#     model.optimize()
#
#     # After optimization, create the matrix for the task-resource assignment
#     allocation_matrix = []
#
#     if model.Status == GRB.OPTIMAL:
#         for i in tasks:
#             row = []
#             for j in resources:
#                 # Sum all subtasks for task i that are assigned to resource j
#                 if sum(b[i, k, j].X for k in subtasks) > 0.5:  # If any subtask is assigned to this resource
#                     row.append(1)
#                 else:
#                     row.append(0)
#             allocation_matrix.append(row)
#
#         # Return the matrix and turnaround time
#         return allocation_matrix, T_turnaround.X
#     else:
#         print("Model is infeasible or not solved.")
#         return None, None













# # TODO working with simplified subtask assign
# def independent_optimization(tasks, subtasks, resources, costs, exec_times, deadlines, budgets, tl):
#     model = Model("IndependentOptimization")
#
#     # Variables: bij = 1 if task i is assigned to resource j
#     b = model.addVars(tasks, resources, vtype=GRB.BINARY, name="b")
#
#     # Total execution times for each task
#     total_exec_times = {
#         i: sum(exec_times[i, k] for k in subtasks) for i in tasks
#     }
#
#     # Total costs for each task
#     total_costs = {
#         i: sum(costs[i, k] for k in subtasks) for i in tasks
#     }
#
#     # Total execution time variable
#     T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")
#
#     # Objective: Minimize weighted sum of cost and execution time
#     obj = 0.5 * (quicksum(total_costs[i] * b[i, j] for i in tasks for j in resources) +
#                  quicksum(total_exec_times[i] * b[i, j] for i in tasks for j in resources)) + 0.5 * T_turnaround
#     model.setObjective(obj, GRB.MINIMIZE)
#
#     # Constraints
#     for i in tasks:
#         # Each task should be assigned to exactly one resource
#         model.addConstr(quicksum(b[i, j] for j in resources) == 1, name=f"Task_{i}_Assignment")
#
#     for j in resources:
#         # Resource capacity constraint (each resource can handle at most one task at a time)
#         model.addConstr(quicksum(b[i, j] for i in tasks) <= 1, name=f"Resource_{j}_Capacity")
#
#     for i in tasks:
#         # Deadline and budget constraints
#         model.addConstr(total_exec_times[i] * quicksum(b[i, j] for j in resources) <= deadlines[i],
#                         name=f"Task_{i}_Deadline")
#         model.addConstr(total_costs[i] * quicksum(b[i, j] for j in resources) <= budgets[i], name=f"Task_{i}_Budget")
#
#     # Turnaround time constraints: Sum of execution time + communication time
#     model.addConstr(T_turnaround >= quicksum(tl) + quicksum(total_exec_times[i] for i in tasks), name="TurnaroundTime")
#
#     # Optimize
#     model.optimize()
#
#     if model.Status == GRB.OPTIMAL:
#         allocation = {i: j for i in tasks for j in resources if b[i, j].X > 0.5}
#         return allocation, T_turnaround.X
#     elif model.Status == GRB.INFEASIBLE:
#         print("Model is infeasible. Relaxing constraints to diagnose issues.")
#         model.computeIIS()  # Identify infeasible subset
#         model.write("model.ilp")  # Save the IIS for inspection
#         return None, None
#     else:
#         print("Optimization problem not solved.")
#         return None, None















# TODO WORKING WITH NO SUBTASKS!!!!!
# def independent_optimization(tasks, resources, costs, exec_times, deadlines, budgets, tl):
#     model = Model("IndependentOptimization")
#     # Variables: bij = 1 if task i is assigned to resource j
#     b = model.addVars(tasks, resources, vtype=GRB.BINARY, name="b")
#
#     # Create a max_exec_time variable for each task
#     max_exec_time = model.addVars(tasks, vtype=GRB.CONTINUOUS, name="max_exec_time")
#     T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")
#
#     # Objective: Minimize weighted sum of cost and execution time
#     obj = 0.5 * (quicksum(costs[i, j] * b[i, j] for i in tasks for j in resources) +
#                  quicksum(exec_times[i, j] * b[i, j] for i in tasks for j in resources)) + 0.5 * T_turnaround
#     model.setObjective(obj, GRB.MINIMIZE)
#
#     # Constraints
#     for i in tasks:
#         # Task assignment constraint (each task is assigned to exactly one resource)
#         model.addConstr(quicksum(b[i, j] for j in resources) == 1, name=f"Task_{i}_Assignment")
#
#     for j in resources:
#         # Resource capacity constraint (each resource can handle at most one task)
#         model.addConstr(quicksum(b[i, j] for i in tasks) <= 1, name=f"Resource_{j}_Capacity")
#
#     for i in tasks:
#         # Deadline and budget constraints
#         model.addConstr(quicksum(exec_times[i, j] * b[i, j] for j in resources) <= deadlines[i],
#                         name=f"Task_{i}_Deadline")
#         model.addConstr(quicksum(costs[i, j] * b[i, j] for j in resources) <= budgets[i], name=f"Task_{i}_Budget")
#
#         # Max execution time for each task based on assigned resources
#         model.addConstr(max_exec_time[i] == quicksum(exec_times[i, j] * b[i, j] for j in resources),
#                         name=f"MaxExecutionTime_{i}")
#
#     # Turnaround time constraints
#     model.addConstr(T_turnaround >= quicksum(tl) + quicksum(max_exec_time[i] for i in tasks),
#                     name="TurnaroundTime")
#
#     # Optimize
#     model.optimize()
#
#     if model.Status == GRB.OPTIMAL:
#         allocation = {i: j for i in tasks for j in resources if b[i, j].X > 0.5}
#         return allocation, T_turnaround.X
#     elif model.Status == GRB.INFEASIBLE:
#         print("Model is infeasible. Relaxing constraints to diagnose issues.")
#         model.computeIIS()  # Identify infeasible subset
#         model.write("model.ilp")  # Save the IIS for inspection
#         return None, None
#     else:
#         print("Optimization problem not solved.")
#         return None, None










# OLD
# def independent_optimization(tasks, resources, costs, exec_times, deadlines, budgets, tl):
#     model = Model("IndependentOptimization")
#     # Variables: bij = 1 if task i is assigned to resource j
#     b = model.addVars(tasks, resources, vtype=GRB.BINARY, name="b")
#     T_turnaround = model.addVar(vtype=GRB.CONTINUOUS, name="T_turnaround")
#
#     # Objective: Minimize weighted sum of cost and execution time
#     obj = 0.5*(quicksum(costs[i, j] * b[i, j] for i in tasks for j in resources) + quicksum(exec_times[i, j] * b[i, j] for i in tasks for j in resources)) + 0.5 * T_turnaround
#     model.setObjective(obj, GRB.MINIMIZE)
#
#     # Constraints
#     for i in tasks:
#         model.addConstr(quicksum(b[i, j] for j in resources) == 1, name=f"Task_{i}_Assignment")
#
#     for j in resources:
#         model.addConstr(quicksum(b[i, j] for i in tasks) <= 1, name=f"Resource_{j}_Capacity")
#
#     for i in tasks:
#         model.addConstr(quicksum(exec_times[i, j] * b[i, j] for j in resources) <= deadlines[i],
#                         name=f"Task_{i}_Deadline")
#         model.addConstr(quicksum(costs[i, j] * b[i, j] for j in resources) <= budgets[i],
#                         name=f"Task_{i}_Budget")
#
#     # Turnaround time constraints
#     model.addConstr(T_turnaround >= quicksum(tl) +
#                     quicksum(exec_times[i, j] * b[i, j] for i in tasks for j in resources),
#                     name="Tturnaround_Sum")
#
#
#     # Auxiliary variable for the max term
#     max_exec_time = model.addVar(vtype=GRB.CONTINUOUS, name="max_exec_time")
#
#     # Constraint to define max_exec_time as the maximum of exec_times[i, j] * b[i, j]
#     for i in tasks:
#         for j in resources:
#             model.addConstr(max_exec_time >= exec_times[i, j] * b[i, j], name=f"MaxExecTime_{i}_{j}")
#
#     # Add the corrected turnaround time constraint
#     model.addConstr(T_turnaround >= max_exec_time + quicksum(tl), name="Tturnaround_Sum")
#
#
#     # model.optimize()
#     # allocation = {i: j for i in tasks for j in resources if b[i, j].X > 0.5}
#     # return allocation, T_turnaround.X if T_turnaround.X else None
#
#     if model.Status == GRB.OPTIMAL:
#         allocation = {i: j for i in tasks for j in resources if b[i, j].X > 0.5}
#         return allocation, T_turnaround.X
#     elif model.Status == GRB.INFEASIBLE:
#         print("Model is infeasible. Relaxing constraints to diagnose issues.")
#         model.computeIIS()  # Identify irreducible infeasible subset
#         model.write("model.ilp")  # Save the IIS for inspection
#         return None, None
#     else:
#         print("Optimization problem not solved.")
#         return None, None

