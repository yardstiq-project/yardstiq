from yardstiq.sdk.module import module

@module(hash="abc123", tags=["dense"])
def create_matrix():    
    return """
@task()
def create_matrix(dataset):
    size = max(max(u, v) for u, v, _ in dataset["content"]) + 1
    matrix = np.zeros((size, size))

    for u, v, weight in dataset["content"]:
        matrix[u, v] = weight
        matrix[v, u] = weight
            
    return matrix
    """

@module(hash="def456", tags=["QAOA", "circuit"])
def create_circuit():
    return """
@task()
def create_circuit(matrix):
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
"""

@module(hash="ghi789", tags=["local"])
def data_loading():
    return """
@task()
def data_loading():
    data = {"version": "1.0", 
            "hash": "abc123", 
            "size": [3, 4], 
            "content": [[0, 1, 1.0], 
                        [1, 2, 2.5], 
                        [2, 3, 1.2], 
                        [3, 0, 0.8]]
            }
    return data
"""

@module(hash="ghi789", tags=["local"])
def run_circuit():
    return """
@task()
def run_circuit(circuit):
    sampler = BackendSamplerV2(backend=AerSimulator())
    transpiled_circuit = transpile(circuit, backend=AerSimulator())
    job = sampler.run([transpiled_circuit])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    return counts
"""
