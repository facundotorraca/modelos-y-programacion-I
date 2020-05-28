import numpy as np

#-----------------------CONSTANTS---------------------------#
ATT_ID = 0
W_TIME = 1
DS_CLR = 2
WASHED = 3
INCOMP = 4
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def _get_more_conflictive(attire_1, attire_2):
    if (attire_1[INCOMP] > attire_2[INCOMP]):
        return attire_1;
    return attire_2;
#-----------------------------------------------------------#

#-----------------------HEURISTICS--------------------------#
def next_slower_attire(attires):
    slower_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[WASHED]:
            slower_attire = attire
            break

    '''
    the conflictives attires (more incompatibilities)
    need to be add at first, so we have a higher prob-
    bability of adding them into a wahing and not on a
    single attire wash
    '''

    for attire in attires:
        if not attire[WASHED]:
            if attire[W_TIME] == slower_attire[W_TIME]:
                slower_attire = _get_more_conflictive(attire, slower_attire)
            elif attire[W_TIME] > slower_attire[W_TIME]:
                slower_attire = attire

    return slower_attire;

def next_more_conflictive_attire(attires):
    more_conflictive_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[WASHED]:
            more_conflictive_attire = attire
            break

    for attire in attires:
        if not attire[WASHED]:
            if attire[INCOMP] >= more_conflictive_attire[INCOMP]:
                more_conflictive_attire = attire

    return more_conflictive_attire;

def next_less_conflictive_attire(attires):
    less_conflictive_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[WASHED]:
            less_conflictive_attire = attire
            break

    for attire in attires:
        if not attire[WASHED]:
            if attire[INCOMP] < less_conflictive_attire[INCOMP]:
                less_conflictive_attire = attire

    return less_conflictive_attire;
#-----------------------------------------------------------#
