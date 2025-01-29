"""Utility functions for generating random circuits."""

import numpy as np

from qiskit.circuit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library.standard_gates import (XGate, HGate, ZGate, CZGate, CCZGate)

def random_circ_params(seed):
    max_operands=3 # maximum operands of each gate (between 1 and 3)

    one_q_ops = [HGate, ZGate] # don't change the order of gate entries
    two_q_ops = CZGate
    three_q_ops = CCZGate
    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    return max_operands, one_q_ops, two_q_ops, three_q_ops, rng


def random_circ_d_const(n: int, d: int, seed=None) -> tuple[QuantumCircuit, QuantumRegister]:
    """Generate random circuit of arbitrary size and form.
    Args:
        n (int): number of quantum wires
        depth (int): layers of operations (i.e. critical path length)
        seed (int): sets random seed (optional) --> set a value to get same circuit on each call
    Returns:
        QuantumCircuit: constructed circuit
    """

    max_operands, one_q_ops, two_q_ops, three_q_ops, rng = random_circ_params(seed)

    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(n)

    prob_num_operands = [[1], [2/3, 1/3], [2/4, 1/4, 1/4]]
    # apply arbitrary random operations at every depth
    for _ in range(d):
        # choose either 1, 2, or 3 qubits for the operation
        remaining_qubits = list(range(n))
        while remaining_qubits:
            max_possible_operands = min(len(remaining_qubits), max_operands)
            num_operands = rng.choice(range(max_possible_operands), p=prob_num_operands[max_possible_operands-1]) + 1
            
            rng.shuffle(remaining_qubits)
            operands = remaining_qubits[:num_operands]
            remaining_qubits = [q for q in remaining_qubits if q not in operands]
            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                operation = two_q_ops
            elif num_operands == 3:
                operation = three_q_ops

            register_operands = [qr[i] for i in operands]
            op = operation()

            qc.append(op, register_operands)
            # qc.barrier()
        qc.barrier()

    return qc, qr

def random_circ_g_const(n: int, g: int, seed=None) -> tuple[QuantumCircuit, QuantumRegister]:
    max_operands, one_q_ops, two_q_ops, three_q_ops, rng = random_circ_params(seed)

    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(n)

    while(g): # setting depth = number of gates
        # choose either 1, 2, or 3 qubits for the operation
        remaining_qubits = list(range(n))
        while remaining_qubits:
            max_possible_operands = min(len(remaining_qubits), max_operands)
            num_operands = rng.choice(range(max_possible_operands)) + 1
            
            rng.shuffle(remaining_qubits)
            operands = remaining_qubits[:num_operands]
            remaining_qubits = [q for q in remaining_qubits if q not in operands]
            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                operation = two_q_ops
            elif num_operands == 3:
                operation = three_q_ops

            register_operands = [qr[i] for i in operands]
            op = operation()

            qc.append(op, register_operands)
            
            g -= 1
            if(g <= 0): break
            
            # qc.barrier()
        qc.barrier()
    return qc, qr


def random_circ_h_const(n: int, h: int, h_prob: float, seed=None) -> tuple[QuantumCircuit, QuantumRegister]:
    """ We don't mind the depth!
        We use a little differnt method here. max_operand is fixed to 3.
    """
    max_operands, one_q_ops, two_q_ops, three_q_ops, rng = random_circ_params(seed)

    qr = QuantumRegister(n, 'q')
    qc = QuantumCircuit(n)
    # h_prob is probability of HGate out of all 4 gates
    prob_num_operands = [[1],
                          [0.5*(h_prob+1), 0.5*(1-h_prob)], 
                          [(h_prob*2+1)/3, (1-h_prob)/3, (1-h_prob)/3]]
    # apply arbitrary random operations at every depth
    """
    remaining_qubits = list(range(n))
    h_count = h
    while h_count > 0:
        max_possible_operands = min(len(remaining_qubits), max_operands)
        num_operands = rng.choice(range(max_possible_operands), p=prob_num_operands[max_possible_operands-1]) + 1
        rng.shuffle(remaining_qubits)
        operands = remaining_qubits[:num_operands]

        if num_operands == 1:
            operation = rng.choice(one_q_ops, p=[h_prob, 1-h_prob])
        elif num_operands == 2:
            operation = two_q_ops
        elif num_operands == 3:
            operation = three_q_ops

        register_operands = [qr[i] for i in operands]
        op = operation()
        qc.append(op, register_operands)
        if operation == HGate:
            h_count -= 1
            qc.barrier()
        """
    h_count = h
    qubits = list(range(n))
    while h_count > 0: # not incomplete, but might be done better to meet requirements
        num_operands = rng.choice(range(max_operands), p=[(h_prob*2+1)/3, (1-h_prob)/3, (1-h_prob)/3]) + 1
        rng.shuffle(qubits)
        operands = qubits[:num_operands]

        if num_operands == 1:
            operation = rng.choice(one_q_ops, p=[h_prob, 1-h_prob])
        elif num_operands == 2:
            operation = two_q_ops
        elif num_operands == 3:
            operation = three_q_ops
        register_operands = [qr[i] for i in operands]
        op = operation()
        qc.append(op, register_operands)
        if operation == HGate:
            h_count -= 1
            qc.barrier() # applying a barrier whenever an HGate is applied
    return qc, qr


"""Utility function to get gate counts, barrier is not counted as a gate"""

# def gate_counts(qc:QuantumCircuit) -> int :
#     """Prints the number of gates in a quantum circuit.
#     This does not include barrier as a gate."""
#     ops_dict = qc.count_ops()
#     gate_counts = sum(ops_dict[gate] for gate in ops_dict.keys())
#     if 'barrier' in ops_dict.keys():
#         gate_counts -= ops_dict['barrier']

#     return gate_counts

# Or 
def gate_counts(qc:QuantumCircuit) -> int :
    return sum(qc.count_ops().values())
