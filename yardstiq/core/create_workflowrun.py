from yardstiq.object.workflow import WorkflowInfo, WorkflowRun
from yardstiq.object import engine_database


def create_workflowrun(workflow_info: WorkflowInfo, engine: str) -> WorkflowRun:
    """Function that take a workflow and uses a engine to run it.
    Engine manager is just to dispatch the workflow to the engine.


    """

    WorkflowRun = engine_database[engine](workflow_info)

    return WorkflowRun
