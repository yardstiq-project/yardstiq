from typing import Any

from yardstiq.object.dataset import Dataset
from yardstiq.object.config import Config
from yardstiq.sdk.module import module
from yardstiq.sdk.algorithm import algorithm
from yardstiq.algorithm.modules.exemple_modules import create_matrix, create_circuit
from yardstiq.algorithm.modules.qall_circuit_executor import run_circuit
from yardstiq.sdk.module import moduleRegistry
import numpy as np
from qiskit import QuantumCircuit

@algorithm(problem="exemple_algorithm", version="1.0.0")
def example_algorithm(config: Config) -> list[module]:
    """Example algorithm that returns a list of callable functions.

    Args:
        config (Config): Configuration parameters for the algorithm.

    Returns:
        list: A list of callable functions.
    """

    # Normally we should use the config in the modules.

    module_0 = moduleRegistry[str, Dataset, ["local"]]

    module_1 = create_matrix

    module_2 = moduleRegistry[np.ndarray, QuantumCircuit, ["QAOA"]]

    module_3 = moduleRegistry[QuantumCircuit, Any, ["run", "local"]]

    return [module_0, module_1, module_2, module_3]
