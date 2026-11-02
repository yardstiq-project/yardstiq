from qall import task


class TaskMod:
    """TaskMod is a wrapper for a module. A module is a callable that contains at least preprocess and postprocess methods and an initialization method. 
    Each process is dispatch on a specific ressource such as CPU, GPU or QPU
    
    Attributes:
        task_config : Configuration of the task to be executed
        module : Module that contains logical methods to be executed for the task
        preprocess : Preprocess method of the module
        postprocess : Postprocess method of the module
    """

    task_config: None
    module: None
    preprocess: None
    postprocess: None

    def __init__(self, module_call: type, mod_kwargs: dict[str, any], task_config: dict[str, any]):
        self.module = module_call(**mod_kwargs)
        self.task_config = task_config

        @task(**self.task_config)
        def _preprocess(data):
            return self.module.preprocess(data)

        @task(**self.task_config)
        def _postprocess(data):
            return self.module.postprocess(data)

        self.preprocess = _preprocess
        self.postprocess = _postprocess

    def preprocess(self, data):
        """Preprocess method of the module"""
        return self.preprocess(data)

    def postprocess(self, data):
        """Postprocess method of the module"""
        return self.postprocess(data)
    
        