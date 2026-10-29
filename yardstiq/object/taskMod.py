


class TaskMod:
    """"""

    task_config: None
    module: None
    preprocess: None
    postprocess: None

    def __init__(self, module_call: type, mod_kwargs: dict[str, Any], task_config: dict[str, Any]):
        self.module = module_call(**mod_kwargs)
        self.task_config = task_config

        