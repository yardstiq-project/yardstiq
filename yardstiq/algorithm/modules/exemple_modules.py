import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz
from yardstiq.object import instance
from yardstiq.object.dataset import Dataset
from qall import task

# from yardstiq.sdk.module import module


# @module(name="create matrix", hash="abc123", tags=["dense"])
@task()
def create_matrix(dataset: dict):
    """Dummy function to create a matrix from input data"""

    size = max(max(u, v) for u, v, _ in dataset["content"]) + 1
    matrix = np.zeros((size, size))

    for u, v, weight in dataset["content"]:
        matrix[u, v] = weight
        matrix[v, u] = weight

    return matrix


# @module(name="create circuit", hash="def456", tags=["QAOA", "circuit"])
@task()
def create_circuit(matrix: np.ndarray):
    """Dummy class to create a circuit from a matrix for testing purposes"""
    n_qubits = matrix.shape[0]
    pauli_list = []
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            if matrix[i, j] != 0:
                pauli_str = ["I"] * n_qubits
                pauli_str[i] = "Z"
                pauli_str[j] = "Z"
                pauli_list.append(("".join(pauli_str[::-1]), matrix[i, j]))

    hamiltonian = SparsePauliOp.from_list(pauli_list)
    ansatz = QAOAAnsatz(hamiltonian, reps=1)
    random_values = np.random.uniform(0, 2 * np.pi, ansatz.num_parameters)
    circuit = ansatz.assign_parameters(random_values)
    circuit.measure_all()

    return circuit


# @module(name="data loading", hash="ghi789", tags=["local"])
@task()
def data_loading(uri: str):
    """Dummy class to load a dataset from a file for testing purposes"""

    data = {
        "version": "1.0",
        "hash": "abc123",
        "size": [3, 4],
        "content": [[0, 1, 1.0], [1, 2, 2.5], [2, 3, 1.2], [3, 0, 0.8]],
    }
    # data = json.load(open(f"{uri}"))
    # dataset = Dataset(name=uri, hash=data["hash"], version=data["version"], content=data["content"])
    return data
