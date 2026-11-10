from qall.core import create_workflow_run
from yardstiq.sdk.engine import engine
from yardstiq.object import algorithm_database
from yardstiq.object.module import Module
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
import typer
from yardstiq.algorithm.exemple_algorithm import example_algorithm
import inspect


@engine("qall")
def qall_engine(workflow: WorkflowInfo) -> WorkflowRun:
    """"""

    algo = algorithm_database[workflow.instance.problem]
    algo_source = create_source(algo[0](workflow.config))

    source = """
    import qall
    import quark
    """ + algo_source

    version = algo[1]

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

    return WorkflowRun(workflow, [], version, run_obj)


def create_source(
    modules: list[Module],
):

    func_defs = []
    core_lines = ["@workflow()", "def example_source():", "    res = None"]

    for module in modules:
        raw, _ = inspect.getsourcelines(module.function)
        clean_lines = [line for line in raw if not line.strip().startswith("@module")]
        source = "".join(clean_lines)

        func_defs.append(f"@task()\n{source}")

        func_name = module.name
        core_lines.append(f"    res = {func_name}(res)")

    res = "\n".join(func_defs) + "\n\n" + "\n".join(core_lines) + "\n"

    return res
