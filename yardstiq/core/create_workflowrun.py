from yardstiq.object.workflow import WorkflowInfo, WorkflowRun
from yardstiq.sdk.engine import EngineRegistry



def create_workflowrun(workflow_info : WorkflowInfo, engine : str) -> WorkflowRun:
    """Function that take a workflow and uses a pipeline to run it. 
    Engine manager is just to dispatch the workflow to the pipeline.

    
    """

    WorkflowRun = EngineRegistry[engine](workflow_info)

    return WorkflowRun

