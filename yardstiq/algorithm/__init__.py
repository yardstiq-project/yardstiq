import importlib
import pkgutil
import json

from yardstiq.core.data_base import cursor
from yardstiq.object.algorithm import Algorithm
from yardstiq.object import algorithm_database

import yardstiq.algorithm.modules as _


def load_all_algorithms():
    """Automatically imports all modules in the current package to ensure that all modules are registered."""
    package_name = __name__
    package_path = __path__

    for _, module_name, _ in pkgutil.walk_packages(package_path):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)


def placeholder_qall(data):
    """qall func to run task using hash"""
    return data


def load_db():
    """Loads all algorithms stored in database"""
    cursor.execute("SELECT id, problem, version, hash FROM algorithms")
    data = cursor.fetchall()

    for row in data:
        algo_id, problem, version, algo_hash = row

        name = ":".join([problem, version])

        algo = Algorithm(
            problem=problem,
            version=version,
            func=placeholder_qall,
            hash=algo_hash,
            local=True,
            name = name
        )

        algorithm_database.register_algorithm(algo)


load_db()
load_all_algorithms()
