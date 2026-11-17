import typer
import inspect
import tempfile

from qall.core import create_workflow_run

from yardstiq.sdk.engine import engine
from yardstiq.object import algorithm_database
from yardstiq.object.algorithm import Algorithm
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
from yardstiq.core.create_source import create_source


@engine("qall")
def qall_engine(workflow: WorkflowInfo) -> WorkflowRun:
    """"""
    algo = algorithm_database[workflow.instance.problem]

    if algo.hash is None:
        return run_new_algo(algo, workflow)
    else:
        print("Feature not ready yet")


def run_new_algo(algo: Algorithm, workflow: WorkflowInfo) -> WorkflowRun:

    algo_source = create_source(algo.func(workflow.config))

    source = """
from qall import task, workflow
#import quark

""" + algo_source

    version = algo.version

    with tempfile.NamedTemporaryFile(mode="w+", delete=True, suffix=".py") as file:
        file.write(source)

        file.flush()

        run_obj = create_workflow_run(
            entrypoint=file.name,
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

    return WorkflowRun(workflow, [], version, run_obj)
