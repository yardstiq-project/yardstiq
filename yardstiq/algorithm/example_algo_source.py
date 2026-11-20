from yardstiq.object import module_database
from yardstiq.sdk.algorithm import algorithm

from qall.object.resource import QpuModality, QpuTopology


@algorithm(
    problem="exemple_algorithm",
    version="1.0.0",
    local=True,
    info=[
        QpuModality.gate_based.value,
        QpuTopology.unknown.name,
        QpuTopology.all_to_all.name,
    ],
)
def example_source(_):
    """ """

    # modules
    data_loading = module_database["data_loading"]

    matrix = module_database["create_matrix"]
    create_circ = module_database["create_circuit"]
    run = module_database["run_circuit"]

    return [data_loading, matrix, create_circ, run]
