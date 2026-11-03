import json

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz

from yardstiq.object import instance
from yardstiq.object.dataset import Dataset

class create_matrix():
    """Dummy class to create a matrix for testing purposes"""

    def preprocess(self, dataset: Dataset) -> np.ndarray:
        """Dummy process method to create a matrix from input data"""

        size = max(max(u, v) for u, v, _ in dataset.content) + 1
        matrix = np.zeros((size, size))

        for u, v, weight in dataset.content:
            matrix[u, v] = weight
            matrix[v, u] = weight
            
        return matrix

    def postprocess(self, data):
        """Dummy postprocess method to process the matrix"""
        
        return data  # Example output

class create_circuit():
    """Dummy class to create a circuit from a matrix for testing purposes"""

    def preprocess(self, matrix: np.ndarray) -> QuantumCircuit:
        """Dummy preprocess method to create a circuit from a matrix"""
        
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
        
    def postprocess(self, data):
        """Dummy postprocess method to process the circuit"""
        
        return data  # Example output

class data_loading():
    """Dummy class to load a dataset from a JSON file for testing purposes"""

    uri : str

    def __init__(self, uri : str):
        self.uri = uri

    def preprocess(self, data) -> Dataset:
        """Load a dataset from a JSON file and return a Dataset object
        
        Args:
            uri (str): The URI of the dataset file."""

        data = json.load(open(f"{self.uri}"))
        dataset = Dataset(name=self.uri, hash=data["hash"], version=data["version"], content=data["content"])
        return dataset

    def postprocess(self, data):
        """Dummy postprocess method to process the dataset"""

        return data
