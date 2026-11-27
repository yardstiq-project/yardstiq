import tempfile
from qall.core.registry import WorkflowSpec
from qall.core import push_workflow_on_registry
from yardstiq.object import Algorithm, Module
from yardstiq.core.create_source import create_source, create_task


def push_algorithm_qall(
    folder: str,
    algorithm: Algorithm,
    requirement: list[str],
) -> str:
    if not requirement:
        requirement = []

    algo_source = create_source(algorithm(None))
    imp = "from qall import task, workflow\nimport qiskit\n"
    for req in requirement:
        imp += f"import {req}\n"

    imp += "\n"
    source = imp + algo_source

    with tempfile.NamedTemporaryFile(
        mode="w+", delete=True, suffix=".py", dir=folder
    ) as file:
        file.write(source)
        file.flush()

        work = WorkflowSpec(file.name)
        tag, dag = push_workflow_on_registry(
            workflow_spec=work,
            workflow_name=algorithm.problem,
            local_only=True,
            workflow_version=algorithm.version,
        )
    return dag.root_hash


def push_module_qall(folder: str, module: Module, requirement: list[str]) -> str:
    source = create_task([module], True)
    imp = "from qall import task\n"
    for req in requirement:
        imp += f"import {req}\n"
        imp += "\n"
        file_source = imp + source

    with tempfile.NamedTemporaryFile(
        mode="w+", delete=True, suffix=".py", dir=folder
    ) as file:
        file.write(file_source)
        file.flush()

        work = WorkflowSpec(file.name)
        tag, dag = push_workflow_on_registry(
            workflow_spec=work,
            workflow_name=module.name,
            local_only=True,
            workflow_version=module.version,
        )
    return dag.root_hash
