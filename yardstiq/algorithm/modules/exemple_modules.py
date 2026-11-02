import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz

class create_matrice():
    """Dummy class to create a matrix for testing purposes"""

    def preprocess(self, dataset: list[tuple[int, int, float]]) -> np.ndarray:
        """Dummy process method to create a matrix from input data"""

        size = max(max(u, v) for u, v, _ in dataset) + 1
        matrice = np.zeros((size, size))
        
        for u, v, weight in dataset:
            matrice[u, v] = weight
            matrice[v, u] = weight
            
        return matrice


    def postprocess(self, data):
        """Dummy postprocess method to process the matrix"""
        
        return data  # Example output


class create_circuit():
    """Dummy class to create a circuit from a matrix for testing purposes"""

    def preprocess(self, matrice: np.ndarray) -> QuantumCircuit:
        """Dummy preprocess method to create a circuit from a matrix"""
        
        n_qubits = matrice.shape[0]
        pauli_list = []
        
        for i in range(n_qubits):
            for j in range(i + 1, n_qubits):
                if matrice[i, j] != 0:
                    pauli_str = ['I'] * n_qubits
                    pauli_str[i] = 'Z'
                    pauli_str[j] = 'Z'
                    pauli_list.append(("".join(pauli_str[::-1]), matrice[i, j]))
                    
        hamiltonian = SparsePauliOp.from_list(pauli_list)
        ansatz = QAOAAnsatz(hamiltonian, reps=1)
        random_values = np.random.uniform(0, 2*np.pi, ansatz.num_parameters)
        circuit = ansatz.assign_parameters(random_values)
        circuit.measure_all()
        
        return circuit
        
    def postprocess(self, data):
        """Dummy postprocess method to process the circuit"""
        
        return data  # Example output

