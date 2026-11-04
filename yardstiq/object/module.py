# from pyparsing import Optional
# from qall import task


# class Module:
#     """Module is a wrapper for a function. A module is a callable that contains at least preprocess and postprocess methods and an initialization method. 
#     Each process is dispatch on a specific ressource such as CPU, GPU or QPU
    
#     Attributes:
#         task_config : Configuration of the task to be executed
#         module : Module that contains logical methods to be executed for the task
#         preprocess : Preprocess method of the module
#         postprocess : Postprocess method of the module
#     """

#     def __init__(self, preprocess: callable, postprocess: Optional[callable] = None):
#         """Initializes a Module with the specified preprocess and postprocess methods.

#         Args:
#             preprocess (callable): The preprocess method of the module.
#             postprocess (callable, optional): The postprocess method of the module. Defaults to None.
#             task_config (dict, optional): Configuration of the task to be executed. Defaults to None.
#         """
#         self.preprocess = preprocess
#         if postprocess is None:
#             self.postprocess = lambda x: x
#         else:
#             self.postprocess = postprocess

#     def preprocess(self, data):
#         """Preprocess method of the module"""
#         return self.preprocess(data)

#     def postprocess(self, data):
#         """Postprocess method of the module"""
#         return self.postprocess(data)


# def moduleRegistry():
#     """ModuleRegistry is a registry that holds all the modules registered in the system."""
#     _modules = {}

#     @classmethod
#     def register_module(cls, name: str, module: Module):
#         """Register a module in the ModuleRegistry.

#         Args:
#             name (str): The name of the module.
#             module (Module): The module to be registered.
#         """
#         cls._modules[name] = module

#     @classmethod
#     def get_module(cls, name: str) -> Module:
#         """Get a module from the ModuleRegistry.

#         Args:
#             name (str): The name of the module.
#         """
#         return cls._modules.get(name)
        