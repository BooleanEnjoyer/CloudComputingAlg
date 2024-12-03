def min_single(a, i, p):
    spelrs = [(j,spelr(a, i, p, j)) for j in resources]
    min_spelr = min(spelrs, key=lambda x: x[1])
    return min_spelr[0] if min_spelr[1] < 0 else -1

def spelr(a, i, p, q):
    a_prim = copy.deepcopy(a)
    a_prim[i][q] += a_prim[i][p]
    a_prim[i][p] = 0
    return (u(a, i) - u(a_prim, i))

def gelr(a, i, p, q):
    a_prim = copy.deepcopy(a)
    a_prim[i][q] += a_prim[i][p]
    a_prim[i][p] = 0
    global_u = sum([u(a, i) for i in tasks])
    global_u_prim = sum([u(a_prim, i) for i in tasks])
    return global_u - global_u_primD

def u(a, i):
    return 1 / max(a[i][j] * exec_times[i, j] * len(mts(a, j)) for j in resources)

def min_global(a, j):
    # gracze jednocześnie używający zasobu j
    mts = mts(a, j)
    # gracze zyskujący na przeniesieniu
    nsts = [] #negative spelr task set
    for i in mts:
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
    res = [i for i in tasks if a[i][j] > 0]
    return res if len(res) > 1 else []

# multiplexing resources of task S_i
def mr(a, i):
    res = [j for j in resources if i in mts(a, j)]
    return res if len(res) > 1 else []

def eval_optimize(a):
    i = 1
    flag = True
    while flag:
        if i == 1:
            flag = False

        # przeciążone zasoby używane przez gracza z indeksem i
        ms = sorted(mr(a, i), key=lambda j: exec_times(i, j), reverse=True)
        for resource_from in ms:
            player = min_global(a, resource_from) # wybór gracza
            if player != -1:
                resource_to = min_single(a, player, resource_from) # wybór zasobu
                ralloc(a, player, resource_from, resource_to) # przeniesienie
                flag = True
        if i == n:
            if flag == False:
                return
            else:
                i = 1
        else:
            i = i + 1

def ralloc(a, i, p, q):
    a[i][q] += a[i][p]
    a[i][p] = 0