from Dependencies.random_circuit_generator import *
from Dependencies.functions_list import *
import random, psutil, time, numpy as np, csv
from mqt import ddsim
from qiskit_aer import StatevectorSimulator

# @calculate_execution_time
def get_random_circ(n=None, d=None, g=None, h=None):
    qc, qr = random_circ_h_const(n, h, 0.1)
    # qc, qr = random_circ_d_const(n, d)
    return qc, qr

""" # Bell State circuit
qc = QuantumCircuit(2)
qc.h([0,1])
qc.cz(0,1)
qc.h(1)
d = qc.depth()
"""

# @calculate_execution_time
def get_stvec(qc, initial_state):
    terms, wire_array = create_poly(qc, n)
    ivs = [j[0] for j in wire_array]
    ovs = [j[-1] for j in wire_array]
    # print("Input variables are: ", ivs)
    # print("Output variables are: ", ovs)
    ttb = truthtable(terms, n, t, initial_state, ivs, np)
    return statevector_(ttb, n, t, ovs, np)
    # counts = {} # : To-Do

def get_stvec_ddsim(qc):
    backend = ddsim.DDSIMProvider().get_backend("statevector_simulator")
    job = backend.run(qc)
    result = job.result()
    return result.get_statevector()

def get_stvec_aer(qc):
    backend = StatevectorSimulator()
    res = backend.run(qc).result()
    return res.get_statevector()

def get_time_poly(qc, initial_state):
    # Time Calculation for Simulation using polynomial equation
    start_cpu_times = psutil.Process().cpu_times()
    start_time = time.time()

    state_vector = get_stvec(qc, initial_state)

    end_cpu_times = psutil.Process().cpu_times()
    end_time = time.time()

    # Calculate user and system CPU times
    user_time = end_cpu_times.user - start_cpu_times.user
    system_time = end_cpu_times.system - start_cpu_times.system
    cpu_time = user_time + system_time
    wall_time = end_time - start_time

    return state_vector, cpu_time, wall_time

def get_time_ddsim(qc):
    # Time Calculation for Simulation using DDSIM by MQT
    start_cpu_times = psutil.Process().cpu_times()
    start_time = time.time()

    state_vector = get_stvec_ddsim(qc)

    end_cpu_times = psutil.Process().cpu_times()
    end_time = time.time()

    # Calculate user and system CPU times
    user_time = end_cpu_times.user - start_cpu_times.user
    system_time = end_cpu_times.system - start_cpu_times.system
    cpu_time = user_time + system_time
    wall_time = end_time - start_time

    return state_vector, cpu_time, wall_time

def get_time_aer(qc):
    # Time Calculation for Simulation using Qiskit's Aer Simulator
    start_cpu_times = psutil.Process().cpu_times()
    start_time = time.time()

    state_vector = get_stvec_aer(qc)

    end_cpu_times = psutil.Process().cpu_times()
    end_time = time.time()

    # Calculate user and system CPU times
    user_time = end_cpu_times.user - start_cpu_times.user
    system_time = end_cpu_times.system - start_cpu_times.system
    cpu_time = user_time + system_time
    wall_time = end_time - start_time

    return state_vector, cpu_time, wall_time

if __name__ == '__main__':
    data = []
    stVectors = []
    for n in range(2, 6):
        for h in range(4, 10):
            # print(f"Value of h: {h}")
            qc, qr = get_random_circ(n=n, h=h)
            n = qc.width()
            h = list(instruction.operation.name for index,
                    instruction in enumerate(qc.data)).count('h')
            d = qc.depth()
            g = gate_counts(qc)
            t = n+h
            # print(f'Value of n: {n}, d: {d}, g: {g}, h: {h}')

            # on variables x0 x1 x2 x3 .... continuosly upto n
            # initial_state = [random.randint(0, 1) for _ in range(n)]
            initial_state = [0 for _ in range(n)]
            # print(f'Initial state of qubits is: {initial_state}')

            stvec_poly, cpu_time_poly, wall_time_poly = get_time_poly(qc, initial_state)
            stvec_ddsim, cpu_time_ddsim, wall_time_ddsim = get_time_ddsim(qc)
            stvec_aer, cpu_time_aer, wall_time_aer = get_time_aer(qc)

            stVectors.append([stvec_poly, stvec_ddsim, stvec_aer])
            data.append([n, h, d, g, t,
                        cpu_time_poly, wall_time_poly,
                        cpu_time_ddsim, wall_time_ddsim,
                        cpu_time_aer, wall_time_aer
                        ])
            
    with open('program_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['n', 'h', 'd', 'g', 't',
                         'cpu_time_poly', 'wall_time_poly',
                         'cpu_time_ddsim', 'wall_time_ddsim',
                         'cpu_time_aer', 'wall_time_aer'
                         ])
        writer.writerows(data)

