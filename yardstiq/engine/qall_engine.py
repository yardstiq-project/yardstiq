import typer
import inspect
import tempfile
import traceback

from qall.core import create_workflow_run, run_workflow
from qall.object.resource import Resource, QpuSpec, QpuModality
from qall.provider.workflow.local import get_local_qpu_resources
from qall.registry import BlockRegistry
from qall.object.task import TaskNode
from qall.object.resource_contraint import QuantumResourceConstraints
from qall.core import run_task

from yardstiq.sdk.engine import engine
from yardstiq.object import algorithm_database
from yardstiq.object.algorithm import Algorithm
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
from yardstiq.core.create_source import create_source
from yardstiq.core.ressources import check_hardware_availability, PROVIDER

DISK = BlockRegistry()


@engine("qall")
def qall_engine(workflow: WorkflowInfo) -> WorkflowRun | None:
    """"""

    if workflow.local == False:
        if PROVIDER == None:
            print("Error: no connection to provider")
            return
        ressources = PROVIDER.list_resources()
    else:
        ressources = get_local_qpu_resources()

    hardware = check_hardware_availability(workflow.config.hardware, ressources)
    if hardware == None:
        typer.echo("Error: Can't find hardware")
        return None

    filters = hardware.qpu
    algos = algorithm_database[workflow.instance.problem]
    res = []
    for algo in algos:
        if check_algo_compatibility(algo, filters):
            res.append(algo)

    s = len(res)
    if s == 0:
        print(
            f"Error: No algorithms found to run {workflow.instance.problem} on {workflow.config.hardware}"
        )
        return None
    elif s > 1:
        selected_algo = res[0]
    else:
        selected_algo = res[0]

    res = None
    if selected_algo.hash == None:
        try:
            res = run_new_algo(selected_algo, workflow)
        except Exception as e:
            print(f"Error reason: {e} ")
            traceback.print_exc()
            return None
    else :
        try:
            res = run_hash(selected_algo, workflow)
        except Exception as e:
            typer.echo(f"Error: {e}")
            traceback.print_exc()
            return None
    return res


def run_hash(algo : Algorithm, workflow : WorkflowInfo) -> WorkflowRun:
    res = run_task(task_hash=algo.hash)
    if res:
        typer.echo(f"Task completed successfully!")
        typer.echo(f"Output artifacts: {len(res)}")

        for artifact in res:
            typer.echo(f"  - {artifact.hash}")

    return WorkflowRun(workflow, versions=algo.version, result=res)

def check_algo_compatibility(algo: Algorithm, q_spec: QpuSpec) -> bool:
    """Check if algorithm follows specification of hardware."""
    contraints = {}

    def get_task_contraint(node_hash: str) -> None:
        task = DISK.get_node_from_local(node_hash)

        for cl, val in task.resources.quantum.to_dict().items():
            if cl not in contraints:
                contraints[cl] = val
            elif cl.startswith("max"):
                contraints[cl] = min(contraints[cl], val)
            elif cl.startswith("min"):
                contraints[cl] = max(contraints[cl], val)

        for child_hash in task.children.values():
            get_task_contraint(child_hash)

    if algo.hash == None:
        return True
    get_task_contraint(algo.hash)

    for key, val in contraints.items():
        if hasattr(q_spec, key):
            elem = getattr(q_spec, key)
            if key.startswith("max") and elem > val:
                return False
            if key.startswith("min") and elem < val:
                return False

    return True


def run_new_algo(algo: Algorithm, workflow: WorkflowInfo) -> WorkflowRun:

    algo_source = create_source(algo.func(workflow.config))

    source = """
from qall import task, workflow
import qiskit

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
            allowed_qpus=[workflow.config.hardware],
            auto_start_daemon=True,
        )

    return WorkflowRun(workflow, version, run_obj)
