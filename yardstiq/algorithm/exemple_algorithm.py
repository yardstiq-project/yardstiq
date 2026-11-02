from yardstiq.object.taskMod import TaskMod
from yardstiq.sdk.algorithm import algorithm
from yardstiq.algorithm.modules.exemple_modules import create_matrice, create_circuit
from yardstiq.algorithm.modules.qall_circuit_executor import qall_circuit_executor


@algorithm(name="exemple_algorithm", version="1.0.0")
def example_algorithm(config: dict) -> list[TaskMod]:
    """Example algorithm that returns a list of callable functions.

    Args:
        config (dict): Configuration parameters for the algorithm.

    Returns:
        list: A list of callable functions.
    """

    # Norammlly we should use the config in the modules.

    module_1 = create_matrice
    module_2 = create_circuit
    module_3 = qall_circuit_executor

    return [TaskMod(module_1, {}, {"min_cpu" : 1, "min_ram_gb" : 2}), TaskMod(module_2, {}, {"min_cpu" : 1, "min_ram_gb" : 2}), TaskMod(module_3, {}, {})]

@algorithm(name="exemple_algorithm2", version="1.0.0")
def example_algorithm(config: dict) -> list[TaskMod]:
    """Example algorithm that returns a list of callable functions.

    Args:
        config (dict): Configuration parameters for the algorithm.

    Returns:
        list: A list of callable functions.
    """

    # Norammlly we should use the config in the modules.

    module_1 = create_matrice
    module_2 = create_circuit
    module_3 = qall_circuit_executor

    return [TaskMod(module_1, {}, {"min_cpu" : 1, "min_ram_gb" : 2}), TaskMod(module_2, {}, {"min_cpu" : 1, "min_ram_gb" : 2}), TaskMod(module_3, {}, {})]