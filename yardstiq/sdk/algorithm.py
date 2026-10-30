from yardstiq.object.algorithm_registry import AlgorithmRegistry


def algorithm():
    """algorithm decorator to register an algorithm in the AlgorithmRegistry. It needs at least a name.

    Args:
        name (str): The name of the algorithm.
    """
    
    def decorator_algorithm(func: callable):
        """decorator function to register an algorithm in the AlgorithmRegistry."""

        algorithm_name = func.__name__

        # Register the algorithm in the AlgorithmRegistry
        AlgorithmRegistry.register_algorithm(algorithm_name, func)

        if func is not None:
            return decorator_algorithm(func)

    return decorator_algorithm