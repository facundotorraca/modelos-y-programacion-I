import numpy as np

# AI -> Attires info [attire_ID | washingtime | washed | incomps | coef]
# IC -> Incompatibilities [attire_ID_1 | attire_ID_2]
# NA -> Number of attires
# NI -> Number of incompatibilities

#-----------------------CONSTANTS---------------------------#
INPUT_FILE = 'segundo_problema.txt'
OUTPUT_FILE = 'output.txt'
COMPATIBLE = 0

W_WEIGHT = 5
I_WEIGTH = 0

ATT_ID = 0
W_TIME = 1
WASHED = 2
INCOMP = 3
COEFIC = 4
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
    coefic = 0 #calculated after loading all attires
    incomps = 0 #calculated after loading all attires
    washed = False #becomes true after adding to a washing
    attire_ID = int(line_spt[1])
    washingtime = int(line_spt[2])
    data["AI"].append([attire_ID, washingtime, washed, incomps, coefic])

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

    print(data['NA'])

    '''
    The graph should be simmetrical.
    If attire a is incompatible with b,
    so, attire b is incom with a
    '''

    #attire_position = attire_ID - 1
    for inc in data['IC']:
        incs[inc[0]-1][inc[1]-1] = 1
        incs[inc[1]-1][inc[0]-1] = 1

    '''
    after the previous step, the matrix has a
    1 if ni nj are incompatible and 0 if
    ni nj are compatible. Now we will change the
    "1" by the number of incompatibilities
    '''

    for i in range(data['NA']):
        for j in range(data['NA']):
            if (incs[i][j] == 1):
                data['AI'][i][INCOMP] += 1

    for i in range(data['NA']):
        for j in range(data['NA']):
            if (incs[i][j] == 1):
                incs[i][j] = data['AI'][i][INCOMP]


    return incs

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

def is_compatible_in_washing(new_attire, washing, incs):
    for attire in washing:
        if incs[attire[ATT_ID] - 1][new_attire[ATT_ID] - 1] != COMPATIBLE:
            return False
    return True

def get_more_conflictive(attire_1, attire_2):
    if (attire_1[INCOMP] > attire_2[INCOMP]):
        return attire_1;
    return attire_2;

def calculate_coeficients(attires):
    for attire in attires:
        attire[COEFIC] = ((attire[W_TIME]*W_WEIGHT) + (attire[INCOMP]*I_WEIGTH))**2
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
                slower_attire = get_more_conflictive(attire, slower_attire)
            elif attire[W_TIME] > slower_attire[W_TIME]:
                slower_attire = attire

    return slower_attire;

def next_more_conflictive_attire(attires):
    conflictive_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[WASHED]:
            conflictive_attire = attire
            break

    for attire in attires:
        if not attire[WASHED]:
            if attire[INCOMP] >= conflictive_attire[INCOMP]:
                conflictive_attire = attire

    return conflictive_attire;

def next_coef_attire(attires):
    curr_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[WASHED]:
            curr_attire = attire
            break

    for attire in attires:
        if not attire[WASHED]:
            if attire[COEFIC] >= curr_attire[COEFIC]:
                curr_attire = attire

    return curr_attire;
#-----------------------------------------------------------#


def optimize_washing_time():
    data = _parse_data(INPUT_FILE)
    incs = _load_incs_matrix(data)

    #calculate_coeficients(data['AI'])

    washings = []

    while not all_attires_are_washed(data['AI']):
        attire = next_slower_attire(data['AI'])

        w_id = 0
        #Add the attire in the posible washing
        while not attire[WASHED]:
            if (w_id >= len(washings)):
                #creates a new washing with the attire
                washings.append([attire])
                attire[WASHED] = True
            else:
                if is_compatible_in_washing(attire, washings[w_id], incs):
                    washings[w_id].append(attire)
                    attire[WASHED] = True
                else:
                    w_id += 1 #Search for next washing

    _print_washings(washings)
    _print_output_file(OUTPUT_FILE, washings)

optimize_washing_time()
