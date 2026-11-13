from yardstiq.object import module_database
from yardstiq.sdk.algorithm import algorithm
from yardstiq.object.config import Config


@algorithm(problem="exemple_algorithm", version="1.0.0", local=True)
def example_source(config: Config):
    """
    Example algorithm that returns a source code as a string to be run on Qall

    Returns:
        str: A string containing the source code of the algorithm.
    """

    module_keys = ["data_loading", "create_matrix", "create_circuit", "run_circuit"]
    modules = [module_database[key] for key in module_keys]

    return modules
