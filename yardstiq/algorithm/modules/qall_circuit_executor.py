from qall import run
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2

class qall_circuit_executor:
    """qall_circuit_executor is a class that can be used to execute a circuit on a QPU/EMU using the qall engine"""

    def preprocess(self, circuit : QuantumCircuit):
        """Dummy preprocess method to process the circuit"""

        # use qall run to run circuit. No implemented yet, just a dummy method to show what to do later

        
        sampler = BackendSamplerV2(backend=AerSimulator())
        transpiled_circuit = transpile(circuit, backend=AerSimulator())
        job = sampler.run([transpiled_circuit])
        result = job.result()
    
        counts = result[0].data.meas.get_counts()
        return counts

    def postprocess(self, data):
        """Dummy postprocess method to process the distribution"""

        return data  # Example output