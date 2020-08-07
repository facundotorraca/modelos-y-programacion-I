import mwcp
import numpy as np

#-----------------------CONSTANTS---------------------------#
ATT_ID = 0
W_TIME = 1
DS_CLR = 2
VSITED = 3
INCOMP = 4

COMPATIBLE = 0
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def _all_attires_are_visited(attires):
    for attire in attires:
        if not attire[VSITED]:
            return False
    return True

def _get_more_conflictive_between(attire_1, attire_2):
    if (attire_1[INCOMP] > attire_2[INCOMP]):
        return attire_1;
    return attire_2;

def _get_slower_between(attire_1, attire_2):
    if (attire_1[W_TIME] > attire_2[W_TIME]):
        return attire_1
    return attire_2

def _next_slower_attire(attires):
    slower_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[VSITED]:
            slower_attire = attire
            break

    for attire in attires:
        if not attire[VSITED]:
            if attire[W_TIME] > slower_attire[W_TIME]:
                slower_attire = attire
            elif attire[W_TIME] == slower_attire[W_TIME]:
                slower_attire = _get_more_conflictive_between(slower_attire, attire)

    return slower_attire

def _next_more_conflictive_attire(attires):
    more_conflictive_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[VSITED]:
            more_conflictive_attire = attire
            break

    for attire in attires:
        if not attire[VSITED]:
            if attire[INCOMP] > more_conflictive_attire[INCOMP]:
                more_conflictive_attire = attire
            elif attire[INCOMP] == more_conflictive_attire[INCOMP]:
                more_conflictive_attire = _get_slower_between(more_conflictive_attire, attire)

    return more_conflictive_attire

def _is_incomp_in_selection(new_att, selection, incs):
    for att in selection:
        if incs[att[ATT_ID]-1][new_att[ATT_ID]-1] == COMPATIBLE:
            return False

    return True
#-----------------------------------------------------------#

#----------------------LOWER-BOUND--------------------------#
def fast_mwcp_method(attires, incs):
    W = []

    for attire in attires:
        W.append(attire[W_TIME])

    MWCP_ITERATIONS = 20000

    # Approx. most heavy clique
    C = mwcp.fast_w_clq(incs, W, MWCP_ITERATIONS)

    lower_bound = 0

    # all the attires that compund a clique
    # finded by the method fast_w_clq.
    clique = []

    for v in C:
        lower_bound += v[mwcp.WEIGHT]
        clique.append(v[mwcp.VERTEX])


    return lower_bound, clique

def append_slowers_method(attires, incs):
    for attire in attires:
        attire[VSITED] = False

    selection = []
    lower_bound = 0

    while not _all_attires_are_visited(attires):
        att = _next_slower_attire(attires)
        att[VSITED] = True

        if _is_incomp_in_selection(att, selection, incs):
            selection.append(att)
            lower_bound += att[W_TIME]

    # all the attires that compound a clique
    # finded by the method fast_w_clq.
    clique = []
    for attire in selection:
        clique.append(attire[ATT_ID])

    for attire in attires:
        attire[VSITED] = False

    return lower_bound, clique

def append_more_conflictive_method(attires, incs):
    for attire in attires:
        attire[VSITED] = False

    selection = []
    lower_bound = 0

    while not _all_attires_are_visited(attires):
        att = _next_more_conflictive_attire(attires)
        att[VSITED] = True

        if _is_incomp_in_selection(att, selection, incs):
            selection.append(att)
            lower_bound += att[W_TIME]

    # all the attires that compound a clique
    # finded by the method fast_w_clq.
    clique = []
    for attire in selection:
        clique.append(attire[ATT_ID])

    for attire in attires:
        attire[VSITED] = False

    return lower_bound, clique
#-----------------------------------------------------------#
