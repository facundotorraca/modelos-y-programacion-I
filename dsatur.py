import numpy as np
import random as rd

#-----------------------CONSTANTS---------------------------#
VERTEX = 0
DEGREE = 1
DS_CLR = 2
DG_SAT = 3
VSITED = 4

UNCOLERED = 0
CONNECTED = 1
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def __get_least_saturating_color(G, V, v, colors):
    vertex = v[VERTEX]

    n = len(V)
    color_saturations = []

    for c in colors:
        c_sat = 0
        for i in range(n):
            if G[vertex][i] == CONNECTED and i != vertex:
                if __vertex_can_use_color(G, V, V[i], c):
                    c_sat += 1
        color_saturations.append(c_sat)

    print(color_saturations)

    c_idx = color_saturations.index(min(color_saturations))
    return colors[c_idx]

def __vertex_can_use_color(G, V, v, c):
    vertex = v[VERTEX]

    n = len(V)

    for i in range(n):
        if G[vertex][i] == CONNECTED and i != vertex:
            if V[i][DS_CLR] == c:
                return False

    return True

def __next_most_saturated_vertex(G, V):
    found = False
    most_saturated_v = None

    for v in V:
        if not v[VSITED] and v[DG_SAT] > 0:
            most_saturated_v = v
            found = True
            break

    if not found:
        return (most_saturated_v, found)

    for v in V:
        if not v[VSITED]:
            if v[DG_SAT] > most_saturated_v[DG_SAT]:
                most_saturated_v = v
            if v[DG_SAT] == most_saturated_v[DG_SAT]:
                most_saturated_v = v if (rd.random() > rd.random()) else most_saturated_v

    return (most_saturated_v, found)

def __next_higher_degree_vertex(G, V):
    higher_degree_v = None

    for v in V:
        if not v[VSITED]:
            higher_degree_v = v
            break

    for v in V:
        if not v[VSITED]:
            if v[DEGREE] >= higher_degree_v[DEGREE]:
                higher_degree_v = v

    return higher_degree_v

def __update_degree_saturation(G, V):
    n = len(V)

    for v in V:
        for i in range(n):
            if G[v[VERTEX]][i] == CONNECTED and v[VERTEX] != i:
                if V[i][DS_CLR] != UNCOLERED:
                    v[DG_SAT] += 1

def __init_vertices(G, V, n):
    for i in range(n):
        V.append([0,0,0,0,0])

    for i in range(n):
        V[i][VERTEX] = int(i)
        V[i][VSITED] = False
        for j in range(n):
            V[i][DEGREE] += int(G[i][j])
#-----------------------------------------------------------#

#--------------------------DSATUR---------------------------#
def _next_vertex(G, V):
    v, found = __next_most_saturated_vertex(G, V)

    if not found:
        v = __next_higher_degree_vertex(G, V)

    return v

def _color_vertex(G, V, v, hc):
    v[VSITED] = True

    n = len(V)
    vertex = v[VERTEX]

    posible_colors = []
    is_posible_color = False

    for color in range(1, hc + 1):
        is_posible_color = True
        for i in range(n):
            if G[vertex][i] == CONNECTED and vertex != i:
                if V[i][DS_CLR] == color:
                    is_posible_color = False
                    break
        if is_posible_color:
            posible_colors.append(color)

    total_colors = len(posible_colors)

    if total_colors == 0:
        v[DS_CLR] = hc + 1
        return hc + 1

    color = __get_least_saturating_color(G, V, v, posible_colors);

    v[DS_CLR] = color
    return color

def _all_visited(V):
    for v in V:
        if not v[VSITED]:
            return False
    return True

def dsatur(G, n):
    V = []
    hc = 1 #highest color

    __init_vertices(G, V, n)


    while not _all_visited(V):
        __update_degree_saturation(G, V)
        v = _next_vertex(G, V)
        c = _color_vertex(G, V, v, hc)
        if c > hc:
            hc = c

    return V
#-----------------------------------------------------------#
