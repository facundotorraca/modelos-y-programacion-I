import heur as hr
import lwbd as lb
import print as pr
import numpy as np
import dsatur as ds

# AI -> Attires info [attire_ID | washingtime | ds_clr | washed | incomp]
# IC -> Incompatibilities [attire_ID_1 | attire_ID_2]
# NI -> Number of incompatibilities
# NA -> Number of attires

#-----------------------CONSTANTS---------------------------#
INPUT_FILE = 'problems/segundo_problema.txt'
OUTPUT_FILE = 'output.txt'
COMPATIBLE = 0

ATT_ID = 0
W_TIME = 1
DS_CLR = 2
WASHED = 3
INCOMP = 4
#-----------------------------------------------------------#

#---------------------LOAD/SAVE-FUNCTION--------------------#
def load_incs_matrix(data):
    incs = np.zeros((data['NA'], data['NA']))

    '''
    The graph should be simmetrical.
    If attire a is incompatible with b,
    so, attire b is incom with a
    '''

    for inc in data['IC']:
        incs[inc[0]-1][inc[1]-1] = 1
        incs[inc[1]-1][inc[0]-1] = 1

    return incs

def calculate_incomps(data, incs):
    for att in data['AI']:
        for i in range(data['NA']):
            att[INCOMP] += incs[att[ATT_ID]-1][i]

def _load_problem_definition(data, line_spt):
    data['NA'] = int(line_spt[2]);
    data['NI'] = int(line_spt[3]);

def _load_incompatibility(data, line_spt):
    attire_ID_1 = int(line_spt[1])
    attire_ID_2 = int(line_spt[2])
    data['IC'].append([attire_ID_1, attire_ID_2])

def _load_attire_info(data, line_spt):
    ds_clr = 0 #dsatur color (asignated after executing DSatur algorithm)
    incomp = 0 #loades after loading incs matrix
    washed = False
    attire_ID = int(line_spt[1])
    washingtime = int(line_spt[2])
    data["AI"].append([attire_ID, washingtime, ds_clr, washed, incomp])

def parse_data(filename):
    data = {'NI': 0, 'NA': 0, 'IC':[], 'AI':[]};

    '''
    reads data from an input file that have the next template:
    * c -> comment | ex: "c this is a comment"
    * p -> problem definition followed by c n m
           "c" is a comment,
           "n" number of attires,
           "m" number of incompatibilities:
            ex: "p edges 10 30"
    * e -> incompatibilitie, follow by n1 n2
           "n1" y "n2" are the attire ID's
    * n -> washing time, follow by n1 c1
           "n1" is attire ID
           "c1" is washing time in seconds
    '''

    with open(filename) as input:
        for line in input:
            line_spt = line.split()

            if line_spt[0] == 'p':
                _load_problem_definition(data, line_spt)

            if line_spt[0] == 'e':
                _load_incompatibility(data, line_spt)

            if line_spt[0] == 'n':
                _load_attire_info(data, line_spt)

    return data
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def all_attires_are_washed(attires):
    for attire in attires:
        if not attire[WASHED]:
            return False
    return True

def is_compatible_by_color(new_attire, washing):
    color_first_attire = washing[0][DS_CLR]

    '''
    All the attires in the washing has the same color
    so we take the color from the first attire.
    '''

    return new_attire[DS_CLR] == color_first_attire

def is_compatible_by_attire(new_attire, washing, incs):
    for attire in washing:
        if incs[attire[ATT_ID] - 1][new_attire[ATT_ID] - 1] != COMPATIBLE:
            return False
    return True
#-----------------------------------------------------------#

#--------------------------WOPS-----------------------------#
def find_solution_greedy(data, incs):
    wid = 0
    washings = []

    while not all_attires_are_washed(data['AI']):
        attire = hr.next_slower_attire(data['AI'])

        wid = 0
        #Add the attire in the posible washing
        while not attire[WASHED]:
            if wid >= len(washings):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if is_compatible_by_attire(attire, washings[wid], incs):
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings

def find_solution_dsatur(data, incs):
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
                if is_compatible_by_color(attire, washings[wid]):
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings

def find_lower_bound(data, incs):
    return lb.append_slowers_method(data['AI'], incs)

def optimize_washing_time():
    data = parse_data(INPUT_FILE)
    incs = load_incs_matrix(data)
    calculate_incomps(data, incs)

    washings = find_solution_dsatur(data, incs)
    lower_bound = find_lower_bound(data, incs)

    pr.print_washings(washings)
    pr.print_lower_bounds(lower_bound)
    pr.print_output_file(OUTPUT_FILE, washings)
#-----------------------------------------------------------#

optimize_washing_time()
