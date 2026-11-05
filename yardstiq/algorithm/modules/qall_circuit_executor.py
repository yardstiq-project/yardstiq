from typing import Any

from qall import task
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2
#from yardstiq.sdk.module import module


#@module(name="run circuit", hash="jkl012", tags=["run", "local"])
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
