"""
This file does not contain the functions needed for universal simulation.
It only includes the funcitons needed for simulating the Clifford + S + T
gates and their inverses.

This file contain all the essential functions required for each step
from creating the polynomial using an array, to returning the final 
state vector after calculating the truth table for each possible values
of variables.
"""

""" Variables default definition
n = number of qubits
t = total number of variables in the equation
max_new_var = name of the next new variable, set to n when no gate is applied. Variable names start from 0.
d = depth of the circuit
wire_array[q] = represents the variable name on qubit q, only used to get ovs for now.
term: array containing polynomial equation 
[x0,x1,x(n-1)] = inital_state variables  

ivs = array of input variables, len(ivs) = n
    Deprecated, use range(n) instead.
ovs = array of output variables, len(ovs) = n
"""

import numpy as np
### Creating the Polynomial array of Circuit
def create_poly(qc, n: int):
    instructions = [(instruction.operation.name,
                    [qc.find_bit(q).index for q in instruction.qubits]) 
                    for index, instruction in enumerate(qc.data)]

    wire_array = [[i] for i in range(n)]
    print("Initial wire_array: ",wire_array) 
    max_new_var = n 
    terms = [] 
    # Each term now also holds a weight, alongside the index of each variable in our polynomial. In form: [weight,[*vars]]

    for operation in instructions:
        # operation is a gate in the format (gate,[q0, q1,...])
        gate = operation[0]
        qubits = operation[1]
        if gate == 'h':
                """
                For H gate on qubit q, expression is x0x1 if the variable names before 
                and after the H gate are x0 and x1 respect. We append the last two 
                variables from the wire_array of qubit q in our polynomial.
                """
                wire_array[qubits[0]].append(max_new_var)
                max_new_var += 1
                # print(f"After applying gate H on qubit {qubits[0]}, wire array is: \n",wire_array)
                terms.append([4,[wire_array[qubits[0]][-2],wire_array[qubits[0]][-1]]]) # Weight for H = 4
        elif gate in ['z','cz','ccz']:
            terms.append([4,[wire_array[j][-1] for j in qubits]]) #Weight for Z, CZ, CCZ = 4; 
            # only additional thing to note is that CZ and CCZ are multi-qubit gates, so they will give higher degree terms

        elif gate == 's':
            terms.append([2,[wire_array[j][-1] for j in qubits]]) #Weight for S = 2

        elif gate == 't':
            terms.append([1,[wire_array[j][-1] for j in qubits]]) #Weight for T = 1
        
        elif gate == 'sdg':
            terms.append([6,[wire_array[j][-1] for j in qubits]]) #Weight for Sdg = 6 = (-2) mod 8

        elif gate == 'tdg':
            terms.append([7,[wire_array[j][-1] for j in qubits]]) #Weight for Tdg = 7 = (-1) mod 8
    t = max_new_var
    return terms, wire_array, t


# function to evaluate polynomial equation
def eval_f(terms,x): 
    # x is an array of type bool, it contains the value of x to be evaluated 
    val_out: int = 0 # gets values between [0,7]
    for term in terms:
        weight = term[0]
        indices = term[1]
        # print("weight and indices: ", weight, indices)
        v = bool(1) # The inputs remain boolean. Hence, the products of the variables will remain boolean. 
        for j in indices:
            v &= x[j] 
        val_out = int(val_out + weight*int(v))%8 #Ensuring all operations are done modulo 8, as integer operations. 
    return val_out

def get_truthtable(terms, n, t, initial_state):
    # in case you don't handle this case yourself
    if n == t: # the program won't come here, I am returning 0 state in main file
        state = "".join([str(int(i)) for i in initial_state])
        print(f"Statevector is: {state} with some global phase")
        return
    # x_range = number of x values possible, given initial_state
    x_range = 2**(t-n) 
    print(x_range)
    """
    Size of truth table, i.e. len(group_size) and len(x_range), is 2**(t-n) because 
    we only have to check for the variables other than the input varialbes becasue 
    values of input variables is fixed given the initial state.
    """
    ttb = np.empty(x_range, dtype=np.uint8) # tt will store value in range [0,7]
    # x = x0 x1 x2 x3 x4 ...
    x = np.empty(t, dtype='bool')
    # y = all variables - input variables == indexes of x(n), x(n+1), x(n+2)...
    y = [i for i in range(t) if i not in range(n)]
    # filling input variables value
    x[0:n] = initial_state # these values are fixed once initial state is known
    for i in range(x_range):
        # i = int(x(n)x(n+1)...)
        # filling other varibles value
        y_bin = bin(i)[2:].zfill(t-n)
        # print(y_bin)
        for ind, val in enumerate(y_bin):
            x[n+ind] = bool(int(val))
        ttb[i] = eval_f(terms,x) # terms is a big array, it should be given as a reference
    return ttb


def get_statevector(ttb, n, t, ovs, starting_index=0):
    # group_size = 2**(t-n) # == size of ttb, 
    # we might consider replacing the values in ttb itself because the ttb is used only once
    s = np.zeros(2**len(ovs),dtype=complex)
    # print(s)
    s_ldic = dict()
    for k in range(0, len(ttb)): # Going through each value
        t_val = ttb[k] # Check truth value for each element
        chosenbits = "".join([ ( bin(k)[2:].zfill(t) )[j] for j in ovs ]) #Choosing the variables which are corresponing to the output. 
        chosen_int = int(chosenbits,2) # Integer value corresponding to chosen variables.  
        # print(k, bin(k)[2:].zfill(t), chosenbits, chosen_int)
        # try: s_ldic[chosen_int][t_val] += 1 
        # except KeyError: 
        #     s_ldic[chosen_int] = np.array([0,0,0,0,0,0,0,0])
        #     s_ldic[chosen_int][t_val] += 1
        if chosen_int not in s_ldic: # !!!!!!! This line is very costly !!!!!!!!!!!
            s_ldic[chosen_int] = np.array([0,0,0,0,0,0,0,0]) 
            # If the chosen variables have not been chosen before, 
            # define a new element corresponding to that combo and then update the array
        s_ldic[chosen_int][t_val] += 1 #If array has been created already, just update it
    print(s_ldic)
    for k in s_ldic:
        # Hardcoded the computation of FFT[1] of the array
        # s_ldic[k] = (s_ldic[k][0] - s_ldic[k][4]) + (s_ldic[k][1] - s_ldic[k][5])/np.sqrt(2)- (s_ldic[k][3] - s_ldic[k][7])/np.sqrt(2) + (1j)*((s_ldic[k][2] - s_ldic[k][6]) + (s_ldic[k][1] - s_ldic[k][5])/np.sqrt(2)+ (s_ldic[k][3] - s_ldic[k][7])/np.sqrt(2) ) 
        s_ldic[k] = (s_ldic[k][0] - s_ldic[k][4]) + np.sqrt(2)*(s_ldic[k][1] - s_ldic[k][5]) + (1j)*((s_ldic[k][2] - s_ldic[k][6]) - np.sqrt(2)*(s_ldic[k][3] - s_ldic[k][7]) ) 
        s[k] = s_ldic[k] 

    stvector = s / (2**0.5)**(t-n) # Normalization
    return stvector


