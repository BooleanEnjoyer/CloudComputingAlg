from gekko import GEKKO


def independent_optimization(tasks, task_subtasks, resources, costs, exec_times, deadlines, budgets, weights, tl):
    wt, we = weights
    def sum(l):
        return m.sum(list(l))

    all_allocation_info = []
    all_allocation_matrix = []
    all_obj_values = []

    for task_index in tasks:
        m = GEKKO(remote=False)
        b = {}
        for i in task_subtasks[task_index]:
            for j in resources:
                b[i, j] = m.Var(value=0, integer=True, lb=0, ub=1, name=f"b_{i}_{j}")
        
        T_turnaround = m.Var(value=0, name="T_turnaround")
        m.Obj(we * sum(costs[task_index, j] * b[i, j] for i in task_subtasks[task_index] for j in resources) + wt * T_turnaround)

        # Constraint 8
        m.Equation(T_turnaround <= deadlines[task_index])

        # Constaint 9
        m.Equation(sum(costs[task_index, j] * b[i, j] for i in task_subtasks[task_index] for j in resources) <= budgets[task_index])

        # Constaint 10
        for i in task_subtasks[task_index]:
            m.Equation(sum(b[i, j] for j in resources) == 1)

        # Constaint 11
        for j in resources:
            m.Equation(sum(b[i, j] for i in task_subtasks[task_index]) <= 1)

        # Constaint 12
        m.Equation(T_turnaround >= sum(tl) + sum(exec_times[task_index, j] * b[i, j] for i in task_subtasks[task_index] for j in resources))

        m.solve(disp=True)

        allocation_info = []
        allocation_matrix = []

        if m.options.SOLVESTATUS == 1:  # Status 1 indicates optimal solution in Gekko
            task_info = f"Task {task_index}:"
            task_row = [0] * len(resources)

            for i in task_subtasks[task_index]:
                assigned_resources = []
                for idx, j in enumerate(resources):
                    if b[i, j].value[0] > 0.5:  # Check if the binary variable is assigned
                        assigned_resources.append(j)
                        task_row[idx] = 1
                task_info += f"\n  Subtask {i} is assigned to Resources: {assigned_resources}"
            
            allocation_info.append(task_info)
            allocation_matrix.append(task_row)

            # Append to the overall results
            all_allocation_info.append("\n".join(allocation_info))
            all_allocation_matrix.append(task_row)
            all_obj_values.append(m.options.OBJFCNVAL)
    
        else:
            print(f"Task {task_index}: Optimization failed or no feasible solution found.")
    
    return all_allocation_info, all_allocation_matrix, all_obj_values