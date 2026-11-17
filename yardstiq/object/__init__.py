from .module import ModuleRegistry
from .algorithm import AlgorithmRegistry
from .engine import EngineRegistry

module_database: ModuleRegistry = ModuleRegistry()
algorithm_database: AlgorithmRegistry = AlgorithmRegistry()
engine_database: EngineRegistry = EngineRegistry()
