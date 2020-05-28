import numpy as np

#-----------------------CONSTANTS---------------------------#
ATT_ID = 0
W_TIME = 1
DS_CLR = 2
VSITED = 3
INCOMP = 4

BOLD = '\033[1m'
ENDC = '\033[0m'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
UNDERLINE = '\033[4m'
#-----------------------------------------------------------#

#----------------------OUTPUT-FUNCTIONS---------------------#
def print_washings(washings):
    print(f"{HEADER}{BOLD}#--------------------------WASHINGS---------------------------#{ENDC}")
    total_w_time = 0
    for i in range(len(washings)):
        w_time = 0
        print(f'WASHING ' + str(i) + ': ', end='')
        for attire in washings[i]:
            print(str(attire[ATT_ID]) + ', ', end='')
            w_time =  w_time if (w_time > attire[W_TIME]) else attire[W_TIME]

        print(f'{OKBLUE}{BOLD}WASHING_TIME:' + str(w_time) + f'{ENDC}')
        total_w_time += w_time
    print(f"{HEADER}{BOLD}#-------------------------------------------------------------#{BOLD}")

    print("\n")
    print(f"{HEADER}{BOLD}#-----------------------WASHING-TIME--------------------------#{ENDC}")
    print('TOTAL_WASHING_TIME: ' + str(total_w_time))
    print(f"{HEADER}{BOLD}#-------------------------------------------------------------#{ENDC}")
    print("\n")

def print_lower_bounds(lower_bound):
    print(f"{HEADER}{BOLD}#-------------------------LOWER-BOUND-------------------------#{ENDC}")
    print("LOWER BOUND:" + str(lower_bound))
    print(f"{HEADER}{BOLD}#-------------------------------------------------------------#{ENDC}")

def print_output_file(filename, washings):
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

    print(f'{OKGREEN}\nSolution saved successfully{ENDC}')
#-----------------------------------------------------------#
