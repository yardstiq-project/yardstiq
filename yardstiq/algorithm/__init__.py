# yardstiq/algorithm/__init__.py
import importlib
import pkgutil


def load_all_algorithms():
    """Automatically imports all modules in the current package to ensure that all algorithms are registered."""
    package_name = __name__
    package_path = __path__

    for _, module_name, _ in pkgutil.walk_packages(package_path):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)


load_all_algorithms()
