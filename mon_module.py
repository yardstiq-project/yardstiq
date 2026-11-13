from yardstiq.sdk.module import module
from yardstiq.sdk.algorithm import algorithm
from yardstiq.object.config import Config
from yardstiq.object import module_database


@module(tags=["local"])
def data_loading_v2(_):
    data = {
        "version": "1.0",
        "hash": "abc123",
        "size": [3, 4],
        "content": [[1, 1, 1.0], [1, 2, 2.5], [2, 3, 1.2], [3, 0, 0.8]],
    }
    return data


@module()
def analyse(counts):
    print(counts)


@algorithm(version="V1")
def externe(_: Config):
    module_keys = [
        "data_loading_v2",
        "create_matrix",
        "create_circuit",
        "run_circuit",
        "analyse",
    ]
    modules = [module_database[key] for key in module_keys]

    return modules
