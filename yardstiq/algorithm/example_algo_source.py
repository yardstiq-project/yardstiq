from yardstiq.sdk.module import module, ModuleRegistry, Module
from yardstiq.sdk.algorithm import algorithm
from yardstiq.object.config import Config



@algorithm(problem="exemple_algorithm", version="1.0.0")
def example_source(config: Config):
    """
    Example algorithm that returns a source code as a string to be run on Qall

    Returns:
        str: A string containing the source code of the algorithm.
    """

    modules = [ModuleRegistry["data_loading"],
    ModuleRegistry["create_matrix"],
    ModuleRegistry["create_circuit"],
    ModuleRegistry["run_circuit"]]

    core = f"""
@workflow()
def example_source():
    res = None   
    """
    func_def = """"""

    for elem in modules:
        func_def = func_def + elem[Module.FUNCTION.value]()
        core = core + f"""
    res = {elem[Module.NAME.value]}(res)
"""

    res = func_def + core

    return res
