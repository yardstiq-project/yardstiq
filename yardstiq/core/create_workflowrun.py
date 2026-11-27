from yardstiq.object.workflow import WorkflowInfo, WorkflowRun
from yardstiq.engine import Qall


def create_workflowrun(workflow_info: WorkflowInfo, engine: str) -> WorkflowRun | None:
    """Function that take a workflow and uses a engine to run it."""

    return Qall.run_workflowinfo(workflow_info)
