import lwbd as lb
import numpy as np
import dsatur as ds

# AI -> Attires info [attire_ID | washingtime | ds_clr | washed | incomp]
# IC -> Incompatibilities [attire_ID_1 | attire_ID_2]
# NI -> Number of incompatibilities
# NA -> Number of attires

#-----------------------CONSTANTS---------------------------#
INPUT_FILE = '../problems/segundo_problema.txt'
OUTPUT_FILE = 'output.txt'
COMPATIBLE = 0

ATT_ID = 0
W_TIME = 1
DS_CLR = 2
WASHED = 3
INCOMP = 4
#-----------------------------------------------------------#

#---------------------LOAD/SAVE-FUNCTIONS--------------------#
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

def _parse_data(filename):
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

def _load_incs_matrix(data):
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

def _calculate_incomps(data, incs):
    for att in data['AI']:
        for i in range(data['NA']):
            att[INCOMP] += incs[att[ATT_ID]-1][i]

def _print_washings(washings):
    total_w_time = 0
    for i in range(len(washings)):
        w_time = 0
        print('WASHING ' + str(i) + ': ', end='')
        for attire in washings[i]:
            print(str(attire[ATT_ID]) + ', ', end='')
            w_time =  w_time if (w_time > attire[W_TIME]) else attire[W_TIME]

        print('WASHING_TIME: ' + str(w_time))
        total_w_time += w_time

    print('\nTOTAL_WASHING_TIME: ' + str(total_w_time))

def _print_lower_bounds(lower_bound):
    print("#-----------------------------#")
    print("LOWER BOUND:" + str(lower_bound))
    print("#-----------------------------#")

def _print_output_file(filename, washings):
    '''
    Cada renglón tiene dos valores separados por un espacio, el primero
    es el número de prenda, el según el número de lavado asignado.
    ej: "1 5" Esto sería lavar la prenda "1" en el lavado "5"
    '''
    with open(filename, 'w') as output_file:
        for i in range(len(washings)):
            w_id = str(i + 1) #start at one the solution
            for attire in washings[i]:
                output_file.write(str(attire[ATT_ID]) + ' ' + w_id + '\n')

    print('Solution saved successfully')
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def all_attires_are_washed(attires):
    for attire in attires:
        if not attire[WASHED]:
            return False
    return True
#-----------------------------------------------------------#

def find_solution(data, incs):
    wid = 0
    washings = []

    #returns vertices colored by DSatur Algorithm
    V = ds.dsatur(incs, data['NA'])

    for v in V:
        data['AI'][v[ds.VERTEX]][DS_CLR] = v[ds.DS_CLR]
        #print(v[ds.DS_CLR])

    for v in V:
        attire = data['AI'][v[ds.VERTEX]]

        wid = 0
        while not attire[WASHED]:
            if (wid >= len(washings)):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if washings[wid][0][DS_CLR] == attire[DS_CLR]:
                    washings[wid].append(attire)
                    attire[WASHED] = True
                else:
                    wid += 1

    return washings

def find_lower_bound(data, incs):
    return lb.append_slowers_method(data['AI'], incs)

def optimize_washing_time():
    data = _parse_data(INPUT_FILE)
    incs = _load_incs_matrix(data)
    _calculate_incomps(data, incs)

    washings = find_solution(data, incs)
    lower_bound = find_lower_bound(data, incs)

    _print_washings(washings)
    _print_lower_bounds(lower_bound)

    _print_output_file(OUTPUT_FILE, washings)

optimize_washing_time()
