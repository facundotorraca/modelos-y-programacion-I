import numpy as np

# AI -> Attires info [attire | washingtime | washed]
# IC -> Incompatibilities [attire_1 | attire_2]
# NA -> Number of attires
# NI -> Number of incompatibilities

#-----------------------CONSTANTS---------------------------#
INPUT_FILE = 'input.txt'
COMPATIBLE = 0

ATT_ID = 0
W_TIME = 1
WASHED = 2
#-----------------------------------------------------------#

#-------------------AUXILIARY-FUNCTIONS---------------------#
def _parse_data(filename):
    data_parsed = {'NI': 0, 'NA': 0, 'IC':[], 'AI':[]};

    with open(filename) as input_file:
        for line in input_file:
            line_splitted = line.split()

            if line_splitted[0] == 'p':
                data_parsed['NI'] = int(line_splitted[2])
                data_parsed['NA'] = int(line_splitted[3])

            if line_splitted[0] == 'e':
                attire_1 = int(line_splitted[1])
                attire_2 = int(line_splitted[2])
                data_parsed["IC"].append([attire_1, attire_2])

            if line_splitted[0] == 'n':
                washed = False
                attire = int(line_splitted[1])
                w_time = int(line_splitted[2])
                data_parsed["AI"].append([attire, w_time, washed])

    return data_parsed

def _load_incs(w_data):
    incs = np.zeros((w_data['NA'], w_data['NA']))

    for inc in w_data['IC']:
        incs[inc[0]][inc[1]] = 1

    return incs
#-----------------------------------------------------------#

#-----------------------HEURISTIC---------------------------#
def all_attires_are_washed(attires):
    for attire in attires:
        if not attire[WASHED]:
            return False
    return True

def next_slower_attire(attires):
    slower_attire = None

    #Find the first not washed attire
    for attire in attires:
        if not attire[WASHED]:
            slower_attire = attire
            break

    for attire in attires:
        if not attire[WASHED]:
            if attire[W_TIME] >= slower_attire[W_TIME]:
                slower_attire = attire

    return slower_attire;

def is_compatible_in_washing(new_attire, washing, incs):
    new_id = new_attire[ATT_ID]

    for attire in washing:
        id = attire[ATT_ID]

        if incs[id][new_id] != COMPATIBLE:
            return False
    return True

def print_washings(washings):
    total_w_time = 0
    for i in range(len(washings)):
        w_time = 0
        print('WASHING ' + str(i) + ': ', end='')
        for attire in washings[i]:
            print(str(attire[ATT_ID]) + ', ', end='')
            w_time += attire[W_TIME]

        print('WASHING_TIME: ' + str(w_time))
        total_w_time += w_time

    print('\nTOTAL_WASHING_TIME: ' + str(total_w_time))


def optimize_washing_time():
    w_data = _parse_data(INPUT_FILE)

    #Load incompatibilities matrix
    incs = _load_incs(w_data)

    washings = []

    while not all_attires_are_washed(w_data['AI']):
        attire = next_slower_attire(w_data['AI'])

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

    print_washings(washings)

optimize_washing_time()
