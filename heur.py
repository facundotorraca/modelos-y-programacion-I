import numpy as np
import dsatur as ds

#-----------------------CONSTANTS---------------------------#
ATT_ID = 0
W_TIME = 1
DS_CLR = 2
WASHED = 3
INCOMP = 4

COMPATIBLE = 0
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def __all_attires_are_washed(attires):
    for attire in attires:
        if not attire[WASHED]:
            return False
    return True

def __get_more_conflictive(attire_1, attire_2):
    if (attire_1[INCOMP] > attire_2[INCOMP]):
        return attire_1;
    return attire_2;

def __is_compatible_by_color(new_attire, washing):
    color_first_attire = washing[0][DS_CLR]

    '''
    All the attires in the washing has the same color
    so we take the color from the first attire.
    '''

    return new_attire[DS_CLR] == color_first_attire

def __is_compatible_by_attire(new_attire, washing, incs):
    for attire in washing:
        if incs[attire[ATT_ID] - 1][new_attire[ATT_ID] - 1] != COMPATIBLE:
            return False
    return True
#-----------------------------------------------------------#

#-----------------------HEURISTICS--------------------------#
def _next_slower_attire(attires):
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
                slower_attire = __get_more_conflictive(attire, slower_attire)
            elif attire[W_TIME] > slower_attire[W_TIME]:
                slower_attire = attire

    return slower_attire;

def _next_more_conflictive_attire(attires):
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

def _next_less_conflictive_attire(attires):
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

#------------------SOLVING-METHODS--------------------------#
def dsatur_method(data, incs):
    wid = 0
    washings = []

    #returns vertices colored by DSatur Algorithm
    V = ds.dsatur(incs, data['NA'])

    for v in V:
        data['AI'][v[ds.VERTEX]][DS_CLR] = v[ds.DS_CLR]

    for v in V:
        attire = data['AI'][v[ds.VERTEX]]

        wid = 0
        #Add the attire in the posible washing
        while not attire[WASHED]:
            if wid >= len(washings):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if __is_compatible_by_color(attire, washings[wid]):
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings

def next_slower_method(data, incs):
    wid = 0
    washings = []

    while not __all_attires_are_washed(data['AI']):
        attire = _next_slower_attire(data['AI'])

        wid = 0
        #Add the attire in the posible washing
        while not attire[WASHED]:
            if wid >= len(washings):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if __is_compatible_by_attire(attire, washings[wid], incs):
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings

def next_more_conflictive_method(data, incs):
    wid = 0
    washings = []

    while not __all_attires_are_washed(data['AI']):
        attire = _next_more_conflictive_attire(data['AI'])

        wid = 0
        #Add the attire in the posible washing
        while not attire[WASHED]:
            if wid >= len(washings):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if __is_compatible_by_attire(attire, washings[wid], incs):
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings

def next_less_conflictive_attire(data, incs):
    wid = 0
    washings = []

    while not __all_attires_are_washed(data['AI']):
        attire = _next_less_conflictive_attire(data['AI'])

        wid = 0
        #Add the attire in the posible washing
        while not attire[WASHED]:
            if wid >= len(washings):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if __is_compatible_by_attire(attire, washings[wid], incs):
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings
#-----------------------------------------------------------#
