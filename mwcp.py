import copy as cp
import time as tm
import numpy as np
import random as rd
from collections import deque

#-----------------------CONSTANTS---------------------------#
K0 = 5

VERTEX = 0
WEIGHT = 1
REMVED = 2

CONNECTED = 1
V_REMOVED = -1
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def __init_vertices(W):
    V = []

    for i in range(len(W)):
        V.append([i, W[i], False])

    return V

def __init_start_set(V):
    start_V_set = []

    for v in V:
        if not v[REMVED]:
            start_V_set.append(v)

    return start_V_set

def __intersect(L1, L2):
    '''
    Recieves two list or vertex L1 and L2 and return the
    intersection between them.
    '''

    I = []

    for u in L1:
        for v in L2:
            if u[VERTEX] == v[VERTEX]:
                I.append(u)

    return I

def __is_empty_graph(G):
    for i in range(len(G)):
        for j in range(len(G)):
            if G[i][j] != V_REMOVED:
                return False

    return True

def __get_most_heavy(V):
    most_heavy = V[0]

    for v in V:
        if v[WEIGHT] > most_heavy[WEIGHT]:
            most_heavy = v

    return most_heavy

def __get_all_neighbors(G, V, v):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a V with all the vertex
    information (ID, weight) and a vertex v (v c V). Return a new list
    with all the vertex from V that are neighbors of v.
    '''

    N = []

    for u in V:
        if G[v[VERTEX]][u[VERTEX]] == CONNECTED:
            N.append(u)

    return N

def __greater_bval_vertex(G, V, candidates):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a V with all the vertex
    information (ID, weight) and a set of candidates. Returns the vertex
    from candidates that has the greater b value. The vertex is removed
    from candidates.
    '''

    b = -1
    v_idx = -1
    greater_bval_v = None

    for u_idx, u in enumerate(candidates):

        curr_b = _get_b(G, V, candidates, u)

        if curr_b > b:
            b = curr_b
            v_idx = u_idx
            greater_bval_v = u

    #remove vertex from candidates
    candidates.pop(v_idx)

    return greater_bval_v
#-----------------------------------------------------------#

#------------------FAST-WCLQ-FUNCTIONS----------------------#
def _reduce_graph(G, V, C):
    C_w = _get_clique_weight(C, V)

    rm_queue = deque()

    for v in V:
        ubv_0, ubv_1 = _get_clique_upper_bound(G, V, v)
        if ubv_0 <= C_w or ubv_1 <= C_w:
            rm_queue.append(v)

    while len(rm_queue) > 0:
        v = rm_queue.popleft()

        N_v = __get_all_neighbors(G, V, v)

        for i in range(len(G)):
            G[v[VERTEX]][i] = V_REMOVED
            G[i][v[VERTEX]] = V_REMOVED

        V[v[VERTEX]][REMVED] = True

        for u in N_v:
            ubv_0, ubv_1 = _get_clique_upper_bound(G, V, u)
            if  ubv_0 <= C_w or ubv_1 <= C_w:
                rm_queue.append(u)

    return G

def _get_clique_weight(C, V):
    '''
    Recieve V with all the vertex information (ID, weight),
    and a clique C. Returns the C weight
    '''

    w = 0

    for v in C:
        w += V[v[VERTEX]][WEIGHT]

    return w

def _adjust_BMS_number(G, k):
    '''
    We start from a small k value (K0), so that the algorithm works fast.
    Whenever start_set becomes empty, which means we do not find a better
    clique with this k value, we adjust k by increasing it as k := 2k, to
    make the algorithm construct cliques in a greedier way. Also, when k
    exceeds a predefined maximum value len(G), it is reset to k := ++k0.
    '''

    new_k = 2 * k

    if new_k > len(G):
        new_k = K0 + 1
        K0 += 1

    return k

def _get_b(G, V, candidates, v):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a V with all the vertex
    information (ID, weight), a set of candidates and a vertex v.
    Returns the b value of the vertex v.
    '''

    N_v = __get_all_neighbors(G, V, v)

    aux = __intersect(candidates, N_v)

    return V[v[VERTEX]][WEIGHT] + _get_clique_weight(aux, V) / 2

def _get_clique_upper_bound(G, V, v):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a V with all the vertex
    information (ID, weight) and a vertex v. Returns an upper bound on
    the weight of any clique containing v is an integer.
    '''

    N_v = __get_all_neighbors(G, V, v)
    # the trivial upper bound is a clique
    # with all v neighbors
    ub_v_0 = _get_clique_weight(N_v, V)

    if len(N_v) == 0:
        return ub_v_0, 0

    u = __get_most_heavy(N_v)
    N_u = __get_all_neighbors(G, V, u)

    ub_v_1a = _get_clique_weight(N_v, V) - u[WEIGHT]
    ub_v_1b = v[WEIGHT] + u[WEIGHT] + _get_clique_weight(__intersect(N_v, N_u), V)

    return ub_v_0, max(ub_v_1a, ub_v_1b)

def _get_add_vertex(G, V, candidates, k):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a V with all the vertex
    information (ID, weight), a set of candidates and a number k.
    Returns the next vertex to be added to the clique.
    '''

    if len(candidates) < k:
        # vertex is removed from candidates inside
        return __greater_bval_vertex(G, V, candidates)

    u_idx = rd.randint(0,len(candidates) - 1)
    u = candidates[u_idx]

    bval = _get_b(G, V, candidates, u)

    for i in range(k):

        v_idx = rd.randint(0,len(candidates) - 1)
        v = candidates[v_idx]

        if _get_b(G, V, candidates, v) > bval:
            u = v
            u_idx = v_idx

    #remove vertex from candidates
    candidates.pop(u_idx)

    return u
#-----------------------------------------------------------#

#-------------------------FAST-WCLQ-------------------------#
def fast_w_clq(G, W, co):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a W with all the vertex
    weight, n is the number of vetices and co, that is the cutoff iterations.
    If the exact solution is not found until co_time, an approximated
    solution is returned. co_time = -1 searchs until the exact solution.
    Returns a set of vertex that compound the most heavy clique found. The set
    is a tuple [(VERTEX, WEIGTH)]. Vertex go from 0 to len(G)-1.
    '''

    G_copy = np.copy(G)

    V = __init_vertices(W)
    #now V has all vertex in a pair [VERTEX, WEIGHT]

    k = K0
    iter = 0

    best_C = [] #best clique inside the graph

    #set of vertex to start the search
    start_V_set = __init_start_set(V)

    while iter < co:

        if len(start_V_set) == 0:
            G = np.copy(G_copy)
            V = __init_vertices(W)
            k = _adjust_BMS_number(G, k)
            start_V_set = __init_start_set(V)

        #pop a random element from the start set
        v = start_V_set.pop(rd.randint(0,len(start_V_set) - 1))

        #creates a new clique
        C = [v]

        #get all the canditates to be part of the clique
        candidates = __get_all_neighbors(G, V, v)

        while len(candidates) != 0:
            #choose a vertex to add from candidates
            #vertex is removed from candidates
            v = _get_add_vertex(G, V, candidates, k)

            N_v = __get_all_neighbors(G, V, v)

            #remove all candidates that are not neighbors of v
            candidates = __intersect(candidates, N_v)

            #current clique weight (includes new vertex weight)
            curr_weight = _get_clique_weight(C, V) + V[v[VERTEX]][WEIGHT]

            #max possible weight that can be added to the clique
            max_possible_weight = _get_clique_weight(candidates, V)

            if curr_weight + max_possible_weight <= _get_clique_weight(best_C, V):
                break

            C.append(v)

        if _get_clique_weight(C, V) >= _get_clique_weight(best_C, V):

            best_C = C
            G = _reduce_graph(G, V, best_C)
            start_V_set = __init_start_set(V)

            if __is_empty_graph(G):
                return best_C #exact solution

        iter += 1

    return best_C
#-----------------------------------------------------------#
