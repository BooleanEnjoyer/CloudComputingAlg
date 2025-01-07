import copy

def genetic_optimization(tasks, resources, exec_times, a_input):
    a = copy.deepcopy(a_input)
    n = len(tasks)

    def min_single(a, i, p):
        spelrs = [(j,spelr(a, i, p, j)) for j in resources if j != p]
        min_spelr = min(spelrs, key=lambda x: x[1])
        return min_spelr[0] if min_spelr[1] < 0 else -1

    def spelr(a, i, p, q):
        a_prim = copy.deepcopy(a)
        a_prim[i-1][q-1] += a_prim[i-1][p-1]
        a_prim[i-1][p-1] = 0
        return (u(a, i) - u(a_prim, i))

    def gelr(a, i, p, q):
        a_prim = copy.deepcopy(a)
        a_prim[i-1][q-1] += a_prim[i-1][p-1]
        a_prim[i-1][p-1] = 0
        global_u = sum([u(a, i) for i in tasks])
        global_u_prim = sum([u(a_prim, i) for i in tasks])
        return global_u - global_u_prim

    def overload_penalty(a, j):
        mts_val = mts(a, j)
        return len(mts_val) if len(mts_val) > 0 else 1 

    def u(a, i):
        t = max(a[i-1][j-1] * exec_times[i, j] * overload_penalty(a, j) for j in resources)
        return 1 / t if t > 0 else 9999999999

    def min_global(a, j):
        # gracze jednocześnie używający zasobu j
        mts_val = mts(a, j)
        # gracze zyskujący na przeniesieniu
        nsts = [] #negative spelr task set
        for i in mts_val:
            q = min_single(a, i, j) # wybór alternatywnego zasobu
            if q != -1:
                spelr_val = spelr(a, i, j, q) # koszt dla danego gracza
                if spelr_val < 0:
                    nsts.append((i, q))

        if len(nsts) == 0:
            return -1
        gelrs = [(i,gelr(a, i, j, q)) for (i, q) in nsts]
        return min(gelrs, key=lambda x: x[1])[0]


    # multiplexing task set of resource j
    def mts(a, j):
        res = [i for i in tasks if a[i-1][j-1] > 0]
        return res if len(res) > 1 else []

    # multiplexing resources of task S_i
    def mr(a, i):
        res = [j for j in resources if i in mts(a, j)]
        return res

    def eval_optimize(a):
        i = 1
        flag = True
        while True:
            if i == 1:
                flag = False

            # przeciążone zasoby używane przez gracza z indeksem i
            ms = sorted(mr(a, i), key=lambda j: exec_times[i, j] * overload_penalty(a, j), reverse=True)
            print(ms, i, n)
            for resource_from in ms:
                player = min_global(a, resource_from) # wybór gracza
                if player != -1:
                    resource_to = min_single(a, player, resource_from) # wybór zasobu
                    ralloc(a, player, resource_from, resource_to) # przeniesienie
                    print(a)
                    flag = True
            if i == n:
                if flag == False:
                    return a
                else:
                    i = 1
            else:
                i = i + 1

    def ralloc(a, i, p, q):
        print(i, p, q)
        a[i-1][q-1] += a[i-1][p-1]
        a[i-1][p-1] = 0
    
    return eval_optimize(a)

# a = [
#     [0, 0, 0, 1, 1],
#     [0, 0, 1, 1, 1],
#     [1, 1, 1, 0, 1]
# ]

# eval_optimize([
#     [0, 0, 0, 1, 1],
#     [0, 0, 1, 1, 1],
#     [1, 1, 1, 0, 1]
# ])

# a_star_prev = [[0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [1, 2, 1, 0, 0]]

# a_star = [[0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [1, 2, 1, 0, 0]]

# print(u(a, 1), u(a_star_prev, 1))
# print(u(a, 2), u(a_star_prev, 2))
# print(u(a, 3), u(a_star_prev, 3))

# print("---------")

# print(u(a_star_prev, 1), u(a_star, 1))
# print(u(a_star_prev, 2), u(a_star, 2))
# print(u(a_star_prev, 3), u(a_star, 3))