from yardstiq.sdk.engine import Engine

class EngineRegistry:
    """EngineRegistry is a class that contains a registry of engines. 
    It allows for the registration and retrieval of engines by name."""

    engines = {}

    @classmethod
    def register_engine(cls, name, engine : Engine):
        cls.engines[name] = engine

    @classmethod
    def get_engine(cls, name):
        return cls.engines.get(name)

    def __class_getitem__(cls, name):
        if name not in cls.engines:
            raise KeyError(f"Engine'{name}' is not registered. Available engines: {list(cls.engines.keys())}")
        return cls.engines[name]
