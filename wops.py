import heur as hr
import lwbd as lb
import print as pr
import numpy as np

# AI -> Attires info [attire_ID | washingtime | ds_clr | washed | incomp]
# IC -> Incompatibilities [attire_ID_1 | attire_ID_2]
# NI -> Number of incompatibilities
# NA -> Number of attires

#-----------------------CONSTANTS---------------------------#
INPUT_FILE = 'problems/primer_problema.txt'
OUTPUT_FILE = 'output.txt'
#-----------------------------------------------------------#

#------------------AUXILIARY-FUNCTIONS----------------------#
def _load_attire_info(data, line_spt):
    ds_clr = 0 #dsatur color (asignated after executing DSatur algorithm)
    incomp = 0 #loades after loading incs matrix
    washed = False
    attire_ID = int(line_spt[1])
    washingtime = int(line_spt[2])
    data["AI"].append([attire_ID, washingtime, ds_clr, washed, incomp])

def _load_incompatibility(data, line_spt):
    attire_ID_1 = int(line_spt[1])
    attire_ID_2 = int(line_spt[2])
    data['IC'].append([attire_ID_1, attire_ID_2])

def _load_problem_definition(data, line_spt):
    data['NA'] = int(line_spt[2]);
    data['NI'] = int(line_spt[3]);
#-----------------------------------------------------------#

#---------------------LOAD/SAVE-FUNCTION--------------------#
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
            att[hr.INCOMP] += incs[att[hrATT_ID]-1][i]
#-----------------------------------------------------------#

#--------------------------WOPS-----------------------------#
def find_solution_greedy(data, incs):
    return hr.dsatur_method(data, incs)

def find_lower_bound(data, incs):
    return lb.fast_mwcp_method(data['AI'], incs)

def optimize_washing_time():
    data = parse_data(INPUT_FILE)
    incs = load_incs_matrix(data)
    calculate_incomps(data, incs)

    washings = find_solution_greedy(data, incs)
    lower_bound = find_lower_bound(data, incs)

    pr.print_washings(washings)
    pr.print_lower_bounds(lower_bound)
    pr.print_output_file(OUTPUT_FILE, washings)
#-----------------------------------------------------------#

optimize_washing_time()
