import numpy as np

#-----------------------CONSTANTS---------------------------#
ATT_ID = 0
W_TIME = 1
DS_CLR = 2
WASHED = 3
INCOMP = 4

COMPATIBLE = 0
#-----------------------------------------------------------#

#-----------------AUXILIARY-FUNCTIONS-----------------------#
def _is_clique(G, C, cs):
    """
    Function to check if the given set
    of vertices in C array is a
    clique or not. The lenght of the
    clique is specified in variable cs
    """

    # Run a loop for all the set of edges
    # for the select vertex
    for i in range(1, cs):
        for j in range(i + 1, cs):

            # If any edge is missing
            if (G[C[i]][C[j]] == COMPATIBLE):
                return False

    return True

def _find_cliques_rec(AC, G, D, C, n, k, i, l) :
    # Check if any vertices from i+1 can be inserted
    for j in range(i + 1, n - (k - l) + 1):

        # If the degree of the graph is sufficient
        if D[j] >= k - 1:

            # Add the vertex to store
            C[l] = j;

            # If the graph is not a clique of size k
            # then it cannot be a clique
            # by adding another edge
            if _is_clique(G, C, l + 1):

                # If the length of the clique is
                # still less than the desired size
                if (l < k):

                    # Recursion to add vertices
                    _find_cliques_rec(AC, G, D, C, n, k, j, l + 1);

                # Size is met
                else :
                    print(C[1:l+1])
                    AC.append(C[1:l+1])
#-----------------------------------------------------------#

#----------------------FIND-CLIQUES-------------------------#
def find_cliques(G, V, minK, maxK):
    '''
    Recieve a G with as a matrix with the connections between vertices
    (1 is connected, 0 is not connected), a V with all the vertex information
    (only vertex degree is important), and a number k, representing the
    minimun size of cloques to be found.
    Returns a list of all cliques of size "k" or more. Each clique is also
    represented as a list of vertices.
    '''

    # number of vertices
    n = len(V)

    # vertices degrees
    D = [0 for i in range(n + 1)]

    # aux for store a clique
    C = [0 for i in range(n + 1)]

    # load degrees for each vertex
    for i in range(n):
        D[i] = V[i][INCOMP]

    # list of all cliques found
    AC = []

    currK = maxK

    while currK >= minK:
        _find_cliques_rec(AC, G, D, C, n, currK, 0, 1)
        currK -= 1

    return AC
#-----------------------------------------------------------#
