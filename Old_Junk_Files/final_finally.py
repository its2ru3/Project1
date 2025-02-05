from Dependencies.random_circuit_generator import *
from Dependencies.functions_list import *
from Elses.TechRaj.exectime import calculate_execution_time
import numpy as np
import random


qc, qr = random_circ_h_const(10, 13, 0.1)
# qc, qr = random_circ_d_const(10, 10)

""" # Bell State circuit
qc = QuantumCircuit(2)
qc.h([0,1])
qc.cz(0,1)
qc.h(1)
d = qc.depth()
"""

n = qc.width()
g = gate_counts(qc)
h = list(instruction.operation.name for index,
          instruction in enumerate(qc.data)).count('h')
d = qc.depth()
t = n+h

def get_statevector(qc, initial_state):
    terms, wire_array = create_poly(qc, n)
    ivs = [j[0] for j in wire_array]
    ovs = [j[-1] for j in wire_array]
    print("Input variables are: ", ivs)
    print("Output variables are: ", ovs)
    ttb = truthtable(terms, n, t, initial_state, ivs, np)
    return statevector_(ttb, n, t, ovs, np)
# counts = {}

# on variables x0 x1 x2 x3 .... continuosly upto n
initial_state = [random.randint(0, 1) for _ in range(n)]
print(initial_state)

print(n, d, g, h)

@calculate_execution_time
def main():
    state_vector = get_statevector(qc, initial_state)
    print(*state_vector, sep=' ')

