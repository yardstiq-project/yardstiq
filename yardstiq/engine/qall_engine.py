from qall.core import create_workflow_run
from yardstiq.sdk.engine import engine
from yardstiq.sdk.algorithm import algorithm
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
from yardstiq.sdk.algorithm import AlgorithmRegistry
import typer
from yardstiq.algorithm.exemple_algorithm import example_algorithm
import os


@engine("qall")
def qall_engine(workflow: WorkflowInfo) -> WorkflowRun:
    """"""

    # algo = AlgorithmRegistry[workflow.instance.problem]
    algo = [example_algorithm, "1.0.0", "yardstiq/algorithm/exemple_algorithm.py"]
    #algorithm = algo[0](workflow.config)
    version = algo[1]

    os.environ["QALL_WORKFLOW_DATASET"] = workflow.instance.dataset

    run_obj = create_workflow_run(
        entrypoint=algo[2],
        workflow_name=None,
        workflow_version=None,
        profile_name=None,
        local_only=True,
        input_artifact_hash=None,
        allowed_cpus=None,
        allowed_gpus=None,
        allowed_qpus=None,
        auto_start_daemon=True,
    )

    #typer.echo(f"Workflow run ID: {run_obj.id}")

    return WorkflowRun(workflow, [], version, run_obj)
