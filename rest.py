from qall import task, workflow

# import quark


@task(requirements=[])
def data_loading(a):
    data = {
        "version": "1.0",
        "hash": "abc123",
        "size": [3, 4],
        "content": [[0, 1, 1.0], [1, 2, 2.5], [2, 3, 1.2], [3, 0, 0.8]],
    }
    return data


@task(requirements=["numpy"])
def create_matrix(dataset):
    import numpy as np

    size = max(max(u, v) for u, v, _ in dataset["content"]) + 1
    matrix = np.zeros((size, size))

    for u, v, weight in dataset["content"]:
        matrix[u, v] = weight
        matrix[v, u] = weight

    return matrix


@task(requirements=["qiskit", "numpy"])
def create_circuit(matrix):
    from qiskit.quantum_info import SparsePauliOp
    from qiskit.circuit.library import QAOAAnsatz
    import numpy as np

    n_qubits = matrix.shape[0]
    pauli_list = []
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            if matrix[i, j] != 0:
                pauli_str = ["I"] * n_qubits
                pauli_str[i] = "Z"
                pauli_str[j] = "Z"
                pauli_list.append(("".join(pauli_str[::-1]), float(matrix[i, j])))

    hamiltonian = SparsePauliOp.from_list(pauli_list)
    ansatz = QAOAAnsatz(hamiltonian, reps=1)
    random_values = np.random.uniform(0, 2 * np.pi, ansatz.num_parameters)
    circuit = ansatz.assign_parameters(random_values)
    circuit.measure_all()
    return circuit


@task(requirements=["qiskit", "qiskit_aer"])
def run_circuit(circuit):
    from qiskit.primitives import BackendSamplerV2
    from qiskit_aer import AerSimulator
    from qiskit import transpile

    sampler = BackendSamplerV2(backend=AerSimulator())
    transpiled_circuit = transpile(circuit, backend=AerSimulator())
    job = sampler.run([transpiled_circuit])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    return counts


@workflow(requirements=["qiskit"])
def example_source():
    res = None
    res = data_loading(res)
    res = create_matrix(res)
    res = create_circuit(res)
    res = run_circuit(res)
