import copy
import time as tm
import numpy as np

#-----------------------CONSTANTS---------------------------#
VERTEX = 0

INCOMPATIBLE = 1
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def _is_comp_in_washing(G, washing, new_a):
    for a in washing:
        if G[new_a - 1][a - 1] == INCOMPATIBLE:
            return False

    return True

def _vertex_added(G, W, a):
    for w in W:
        if a in w:
            return True
    return False

def _add_to_washing(G, W, a):
    if _vertex_added(G, W, a):
        return

    added = False
    for w in W:
        if _is_comp_in_washing(G, w, a):
            w.append(a)
            added = True
            break

    if not added:
        W.append([a])

def _all_vertex_added(W, n):
    att_added = 0;

    for washing in W:
        att_added += len(washing)

    return att_added == n
#-----------------------------------------------------------#


#------------------SAVE/INIT-FUNCTIONS----------------------#
def __save_solution(W, R):
    if W in R:
        return
    R.append(copy.deepcopy(W))

def __init_vertices(G, V, n):
    for i in range(n):
        V.append(int(i) + 1)

def __pop_vertex(W, a):
    idx = 0;
    for washing in W:
        if a in washing:
            # a is always last element added
            washing.pop()
            if len(washing) == 0:
                W.pop(idx)
            break
        idx += 1
#-----------------------------------------------------------#

def recbt(G, V, R, W, n, s):
    if len(R) == s:
        return

    if _all_vertex_added(W, n):
        __save_solution(W, R)
        return

    for i, v in enumerate(V):
        W_copy = copy.deepcopy(W);
        _add_to_washing(G, W_copy, v)

        recbt(G, V[:i] + V[i+1:], R, W_copy, n, s)

def backtracking(G, n, s):
    V = []
    W = [] # washings
    R = [] # all washings generated

    __init_vertices(G, V, n)


    recbt(G, V, R, W, n, s)

    for r in R:
        print(r)
    return R
