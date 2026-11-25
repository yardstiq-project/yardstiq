from yardstiq.sdk.module import module
from qall import run


@module(tags=["dense"], qall_args={"requirements": ["numpy"]}, local=True)
def create_matrix(dataset):
    import numpy as np

    size = max(max(u, v) for u, v, _ in dataset["content"]) + 1
    matrix = np.zeros((size, size))

    for u, v, weight in dataset["content"]:
        matrix[u, v] = weight
        matrix[v, u] = weight

    return matrix


@module(
    tags=["QAOA", "circuit"],
    qall_args={
        "requirements": ["qiskit", "numpy"],
    },
    local=True,
)
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


@module(tags=["local"], local=True)
def data_loading(n: int | None, densite=0.5):
    """
    Génère les données pour un graphe QAOA.

    :param n: La taille (nombre de nœuds ou qubits).
    :param densite: Probabilité (entre 0 et 1) d'avoir une connexion entre deux nœuds.
    :return: Dictionnaire contenant les métadonnées et la structure du graphe.
    """
    import random
    import hashlib
    import time

    content = []
    if n == None:
        n = 5

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < densite:
                poids = round(random.uniform(0.5, 3.0), 1)
                content.append([i, j, poids])

    if not content and n > 1:
        content.append([0, 1, 1.0])

    hash_str = hashlib.md5(str(time.time()).encode()).hexdigest()[:6]

    data = {
        "version": "1.0",
        "hash": hash_str,
        "size": [n, len(content)],
        "content": content,
    }

    return data


@module(
    tags=["local"],
    qall_args={
        "requirements": ["qiskit", "qiskit-aer"],
    },
    local=True,
)
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
