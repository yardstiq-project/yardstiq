

from yardstiq.sdk.algorithm import algorithm

class AlgorithmRegistry:
    """AlgorithmRegistry is a registry that holds all the algorithms registered in the system."""

    _algorithms = {}

    @classmethod
    def register_algorithm(cls, name: str, func: callable):
        """Register an algorithm in the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm.
            func (callable): The function that implements the algorithm.
        """
        cls._algorithms[name] = func

    @classmethod
    def get_algorithm(cls, name: str) -> callable:
        """Get an algorithm from the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm."""
        return cls._algorithms.get(name)

    @classmethod
    def __class_getitem__(cls, name):
        if name not in cls._algorithms:
            raise KeyError(f"Algorithm '{name}' is not registered. Available algorithms: {list(cls._algorithms.keys())}")
        return cls._algorithms[name]