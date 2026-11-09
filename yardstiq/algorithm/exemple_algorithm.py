import qall
import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz
from qall import task
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2





@task()
def run_circuit(circuit: QuantumCircuit):
    """Dummy function to run a circuit on a QPU/EMU using the qall engine"""

    # use qall run to run circuit. No implemented yet, just a dummy method to show what to do later

    sampler = BackendSamplerV2(backend=AerSimulator())
    transpiled_circuit = transpile(circuit, backend=AerSimulator())
    job = sampler.run([transpiled_circuit])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    return counts

@task()
def create_matrix(dataset: dict):
    """Dummy function to create a matrix from input data"""

    size = max(max(u, v) for u, v, _ in dataset["content"]) + 1
    matrix = np.zeros((size, size))

    for u, v, weight in dataset["content"]:
        matrix[u, v] = weight
        matrix[v, u] = weight
            
    return matrix

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

@task()
def data_loading(uri : str):
    """Dummy class to load a dataset from a file for testing purposes"""        

    data = {"version": "1.0", 
            "hash": "abc123", 
            "size": [3, 4], 
            "content": [[0, 1, 1.0], 
                        [1, 2, 2.5], 
                        [2, 3, 1.2], 
                        [3, 0, 0.8]]
            }
    return data



@qall.workflow()
def example_algorithm():
    """Example algorithm that returns a list of callable functions.

    Args:
        config (Config): Configuration parameters for the algorithm.

    Returns:
        list: A list of callable functions.
    """
    modules = [data_loading, create_matrix, create_circuit, run_circuit]

    res = "test"
    for module in modules:
        if not callable(module):
            raise TypeError(f"Module '{module.__name__}' is not callable.")
        res = module(res)

