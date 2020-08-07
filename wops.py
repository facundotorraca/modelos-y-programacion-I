import sys
import heur as hr
import lwbd as lb
import time as tm
import print as pr
import numpy as np
import writer as wt
import clique as clq

# AI -> Attires info [attire_ID | washingtime | ds_clr | washed | incomp]
# IC -> Incompatibilities [attire_ID_1 | attire_ID_2]
# NI -> Number of incompatibilities
# NA -> Number of attires

#-----------------------CONSTANTS---------------------------#
INPUT_FILE = 'problems/tercer_problema.txt'
CLIQUES_FILE = 'clq_3.txt'
SOLUTION_FILE = 'sol_3.txt'
CPLEX_MOD_FILE = 'mdl_3.mod'

NORML_MODE = "--norml"
CPLEX_MODE = "--cplex"
TWICE_MODE = "--twice"
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
            att[hr.INCOMP] += incs[att[hr.ATT_ID]-1][i]
#-----------------------------------------------------------#

#--------------------------WOPS-----------------------------#
def find_solution_greedy(data, incs):
    start_time = tm.time()
    washings = hr.next_slower_method(data, incs)
    exec_time = tm.time() - start_time
    return washings, exec_time

def find_lower_bound(data, incs):
    start_time = tm.time()
    lower_bound, lw_clique = lb.fast_mwcp_method(data['AI'], incs)
    exec_time = tm.time() - start_time
    return lower_bound, lw_clique, exec_time

def find_range_cliques(data, incs, minK, maxK):
    start_time = tm.time()
    cliques = clq.find_cliques(incs, data['AI'], minK, maxK)
    exec_time = tm.time() - start_time
    return cliques, exec_time

def optimize_washing_time(mode, minClq, maxClq):
    data = parse_data(INPUT_FILE)
    incs = load_incs_matrix(data)
    calculate_incomps(data, incs)

    if mode == CPLEX_MODE or mode == TWICE_MODE:
        wt.write_cplex_mod(data, incs, CPLEX_MOD_FILE)

    if mode != NORML_MODE and mode != TWICE_MODE:
        return

    # avoid search trivial cliques of two vertices
    minClq = 3 if minClq == None else minClq

    # maxK is default 10 percent of the size of the graph
    maxClq = int(0.1 * data['NA']) if maxClq == None else maxClq

    washings, sl_time = find_solution_greedy(data, incs)
    lower_bound, lw_clique, lw_time = find_lower_bound(data, incs)
    cliques, clq_time = find_range_cliques(data, incs, minClq, maxClq)

    pr.print_washings(washings, sl_time)
    pr.print_solution_file(SOLUTION_FILE, washings)
    pr.print_lower_bounds(lower_bound, lw_time)
    pr.print_cliques_to_file(CLIQUES_FILE, minClq, maxClq, cliques, clq_time)
#-----------------------------------------------------------#

if  __name__ == "__main__" :
    mode = NORML_MODE
    minClq = None
    maxClq = None

    if len(sys.argv) >= 2:
        mode = sys.argv[1]

    if len(sys.argv) >= 3:
        minClq = int(sys.argv[2])

    if len(sys.argv) >= 4:
        maxClq = int(sys.argv[3])

    optimize_washing_time(mode, minClq, maxClq)
