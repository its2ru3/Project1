import random
from qiskit import QuantumCircuit
from qiskit.circuit.library import CCZGate

n_qubits = 20
depth = 100
gate_set = ['h', 'z', 'cz', 'ccz', 't', 's', 'tdg', 'sdg']

qc = QuantumCircuit(n_qubits)
for _ in range(depth):
    g = random.choice(gate_set)
    if g == 'h':
        qc.h(random.randrange(n_qubits))
    elif g == 'z':
        qc.z(random.randrange(n_qubits))
    elif g == 'cz':
        q1, q2 = random.sample(range(n_qubits), 2)
        qc.cz(q1, q2)
    elif g == 'ccz':
        if n_qubits >= 3:
            q1, q2, q3 = random.sample(range(n_qubits), 3)
            qc.append(CCZGate(), [q1, q2, q3])
    elif g == 't':
        qc.t(random.randrange(n_qubits))
    elif g == 's':
        qc.s(random.randrange(n_qubits))
    elif g == 'tdg':
        qc.tdg(random.randrange(n_qubits))
    elif g == 'sdg':
        qc.sdg(random.randrange(n_qubits))