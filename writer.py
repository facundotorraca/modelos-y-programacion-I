# TIPES OF VARIABLES:
# wtm_w -> this variable counts the washing time of the washing w
# n_a_w -> the attire a goes in the washing w [binary 0,1]

# TIPES OF CONSTRAITS:
# incs -> incompatibilites between attires
# unqs -> uniqueness of each attire in all washings
# time -> count the washing time of each washing

#-----------------------CONSTANTS---------------------------#
COMPATIBLE = 0

ATT_ID = 0
W_TIME = 1
DS_CLR = 2
WASHED = 3
INCOMP = 4

INTPVAR = "dvar int+ "    # positive integer for CPLEX
BOOLVAR = "dvar boolean " # boolean variable for CPLEX
ENDLINE = ";\n"           # end code line and jump
#-----------------------------------------------------------#

#------------------------CPLEX-DIVISORS---------------------#
VAR_DIVISOR = "//------------------------VARIABLES-----------------------//"
OBJ_DIVISOR = "//------------------------OBJECTIVE-----------------------//"
CTR_DIVISOR = "//-----------------------CONSTRAITS-----------------------//"
GEN_DIVISOR = "//--------------------------------------------------------//"
#-----------------------------------------------------------#

#----------------------VARS-AUXILIARY-----------------------#
def __gen_N_A_W_varname(a, w):
    return "n_" + str(a) + "_" + str(w)

def __gen_WTM_W_varname(w):
    return "wtm_" + str(w)

def __write_N_A_W_vars(data, output):
    for a in range(1, data["NA"] + 1):
        for w in range(1, data["NA"] + 1):

            varname = __gen_N_A_W_varname(a, w)
            output.write(BOOLVAR + varname + ENDLINE)

        output.write("\n")

def __write_WTM_W_vars(data, output):
    for w in range(1, data["NA"] + 1):

        varname = __gen_WTM_W_varname(w)
        output.write(INTPVAR + varname + ENDLINE)
#-----------------------------------------------------------#

#-------------------CONSTRAIT-AUXILIARY---------------------#
def __gen_inc_constrait_name(a1, a2, w):
    return "inc_" + str(a1) + "_" + str(a2) + "_w" + str(w)

def __gen_inc_constrait(a1, a2, w):
    n_a1_w = __gen_N_A_W_varname(a1, w)
    n_a2_w = __gen_N_A_W_varname(a2, w)
    return n_a1_w + " + " + n_a2_w + " <= 1" + ENDLINE

def __write_attire_inc_constrait(a1, a2, num_washes, output):
    for w in range(1, num_washes + 1):
        ctr = __gen_inc_constrait(a1, a2, w)
        ctrname = __gen_inc_constrait_name(a1, a2, w)
        output.write("\t" + ctrname + ": " + ctr)

def __write_incs_constraits(data, incs, output):
    num_wsh = data["NA"]

    """
    To reduce de number of constraits of the model,
    the matrix is going to be looped in a diagonal way.
    This will reduce the number of constraits in 50%.
    For example, if "e 1 3" the "e 3 1" (simetrical matrix),
    but the only restriction that we will have is
    n_1_w + n_3_w == 1 and not also n_3_w + n_1_w == 1
    """

    for i in range(data["NA"]):
        for j in range(data["NA"]):

            if j <= i:
                continue

            if incs[i][j] != COMPATIBLE:
                __write_attire_inc_constrait(i + 1, j + 1, num_wsh, output)

        output.write("\n")


def __gen_unq_constrait_name(a):
    return "unq_" + str(a)

def __gen_unq_constrait(a, num_washes):
    ctr = ""

    for w in range(1, num_washes + 1):
        ctr += __gen_N_A_W_varname(a, w)

        if w <= num_washes - 1:
            ctr += " + "

    ctr += " == 1"
    ctr += ENDLINE

    return ctr

def __write_unqs_constraits(data, output):
    num_wsh = data["NA"] # number of washes

    for a in range(1, data["NA"] + 1):

        ctr = __gen_unq_constrait(a, num_wsh)
        ctrname = __gen_unq_constrait_name(a)

        output.write("\t" + ctrname + ": " + ctr)

    output.write("\n")


def __gen_time_constrait(w, a, data):
    w_time = data["AI"][a - 1][W_TIME]

    n_a_w = __gen_N_A_W_varname(a, w)
    wtm_w = __gen_WTM_W_varname(w)


    ctr = wtm_w + " >= " + str(w_time) + \
          " * " + str(n_a_w) + ENDLINE

    return ctr

def __gen_time_constrait_name(w, a):
    return "wtime_"  + str(w) + "_if_" + str(a)

def __write_time_constraits(data, output):
    num_wsh = data["NA"]

    for w in range(1, num_wsh + 1):
        for a in range(1, data["NA"] + 1):

            ctr = __gen_time_constrait(w, a, data)
            ctrname = __gen_time_constrait_name(w, a)
            output.write("\t" + ctrname + ": " + ctr)

        output.write("\n")
#-----------------------------------------------------------#

#--------------------AUXILIARY-FUNCTIONS--------------------#
def _write_variables(data, output):
    output.write("\n" + VAR_DIVISOR + "\n")

    __write_N_A_W_vars(data, output)
    __write_WTM_W_vars(data, output)

    output.write(GEN_DIVISOR + "\n")

def _write_objective(data, output):
    output.write("\n" + OBJ_DIVISOR + "\n")

    output.write("minimize \n")

    for w in range(1, data["NA"] + 1):
        varname = __gen_WTM_W_varname(w)
        output.write(varname)

        delim = " + "
        if w == data["NA"]:
            delim = ENDLINE

        output.write(delim)


    output.write(GEN_DIVISOR + "\n")

def _write_constrait(data, incs, output):
    output.write("\n" + CTR_DIVISOR + "\n")

    output.write("subject to {\n")
    __write_incs_constraits(data, incs, output)
    __write_unqs_constraits(data, output)
    __write_time_constraits(data, output)
    output.write("}\n")

    output.write(GEN_DIVISOR + "\n")
#-----------------------------------------------------------#

#--------------------------WRITES---------------------------#
def write_cplex_mod(data, incs, filename):
    with open(filename, "w") as output:
        output.write("using CPLEX;\n")

        _write_variables(data, output)
        _write_objective(data, output)
        _write_constrait(data, incs, output)
#-----------------------------------------------------------#
