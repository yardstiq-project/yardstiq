from yardstiq.object.workflow import WorkflowInfo, WorkflowRun
from yardstiq.object.engine_registry import EngineRegistry


def engine_manager(workflow : WorkflowInfo, pipeline : str) -> WorkflowRun:
    """Function that take a workflow and uses a pipeline to run it. 
    Engine manager is just to dispatch the workflow to the pipeline.

    
    """

    WorkflowRun = EngineRegistry[pipeline](workflow)

    return WorkflowRun

