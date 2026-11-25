import importlib
import pkgutil
import json

from yardstiq.database.data_base import cursor
from yardstiq.object.module import Module
from yardstiq.object import module_database


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
    """Loads all modules stored in database"""
    cursor.execute("SELECT id, name, version, hash, tags FROM modules")
    data = cursor.fetchall()

    for row in data:
        module_id, name, version, module_hash, tags_str = row

        try:
            tags = json.loads(tags_str) if tags_str else []
        except json.JSONDecodeError:
            tags = []

        module = Module(
            name=name,
            function=placeholder_qall,
            version=version,
            local=True,
            tags=tags,
            qall_args={},
            hash=module_hash,
        )

        module_database.register_module(module)


load_all_algorithms()
load_db()
