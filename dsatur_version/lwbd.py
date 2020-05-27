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

def _get_more_conflictive(attire_1, attire_2):
    if (attire_1[INCOMP] > attire_2[INCOMP]):
        return attire_1;
    return attire_2;

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
                slower_attire = _get_more_conflictive(slower_attire, attire)

    return slower_attire;

def _is_incomp_in_selection(new_att, selection, incs):
    for att in selection:
        if incs[att[ATT_ID]-1][new_att[ATT_ID]-1] == COMPATIBLE:
            return False

    return True
#-----------------------------------------------------------#

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

    for attire in attires:
        attire[VSITED] = False

    return lower_bound
