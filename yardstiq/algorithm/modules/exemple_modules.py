import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz
from yardstiq.object import instance
from yardstiq.object.dataset import Dataset
from qall import task
from yardstiq.sdk.module import module


@module(input_type=Dataset, output_type=np.ndarray, tag=["dense"])
@task()
def create_matrix(dataset: Dataset):
    """Dummy function to create a matrix from input data"""

    size = max(max(u, v) for u, v, _ in dataset.content) + 1
    matrix = np.zeros((size, size))

    for u, v, weight in dataset.content:
        matrix[u, v] = weight
        matrix[v, u] = weight
            
    return matrix

@module(input_type=np.ndarray, output_type=QuantumCircuit, tag=["QAOA, circuit"])
@task()
def create_circuit(matrix: np.ndarray):
    """Dummy class to create a circuit from a matrix for testing purposes"""        
    n_qubits = matrix.shape[0]
    pauli_list = []        
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            if matrix[i, j] != 0:
                pauli_str = ['I'] * n_qubits
                pauli_str[i] = 'Z'
                pauli_str[j] = 'Z'
                pauli_list.append(("".join(pauli_str[::-1]), matrix[i, j]))
                    
    hamiltonian = SparsePauliOp.from_list(pauli_list)
    ansatz = QAOAAnsatz(hamiltonian, reps=1)
    random_values = np.random.uniform(0, 2*np.pi, ansatz.num_parameters)
    circuit = ansatz.assign_parameters(random_values)
    circuit.measure_all()
         
    return circuit

@module(input_type=str, output_type=Dataset, tag=["local"])
@task()
def data_loading(uri : str):
    """Dummy class to load a dataset from a file for testing purposes"""        
    data = json.load(open(f"{uri}"))
    dataset = Dataset(name=uri, hash=data["hash"], version=data["version"], content=data["content"])
    return dataset
