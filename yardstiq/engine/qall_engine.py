import logging
import tempfile
import textwrap

from qall.core import create_workflow_run, run_task, run
from qall.object.resource import QpuSpec, Resource
from qall.provider.workflow.local.local_provider import LocalWorkflowProviderClient
from qall.registry import BlockRegistry
from yardstiq.core.create_source import create_source
from yardstiq.core.resources import WorkflowProviderClient, log_to_provider
from yardstiq.object import Algorithm, Engine
from yardstiq.object.workflow import WorkflowInfo, WorkflowRun
from yardstiq.registry import algorithm_database

logger = logging.getLogger(__name__)
DISK = BlockRegistry()
LOCAL_RESOURCES = LocalWorkflowProviderClient()


class Qall(Engine):
    name: str = "qall"

    @classmethod
    def run_workflowinfo(cls, workflow: WorkflowInfo) -> WorkflowRun | None:
        provider = log_to_provider()

        try:
            resources = cls._get_resources(workflow.local, provider)
            resource = cls._check_availability(workflow.config.hardware, resources)
            algorithm = cls._get_algorithm(workflow.instance.problem, resource.qpu)
        except Exception as e:
            logger.error("Failed to prepare workflow execution: %s", e)
            return None

        try:
            if not algorithm.hash:
                return cls._run_algorithm_source(algorithm, resource, workflow)
            return cls._run_algorithm_hash(algorithm, resource, workflow)
        except Exception:
            logger.exception("Failed to execute algorithm %s", algorithm.version)
            return None

    @classmethod
    def _get_algorithm(cls, problem: str, filters: QpuSpec) -> Algorithm:
        algorithms = algorithm_database[problem]
        compatible_algos = [
            algo for algo in algorithms if cls._check_algo_compatibility(algo, filters)
        ]

        if not compatible_algos:
            raise LookupError(
                f"No algorithms found to run '{problem}' on '{filters.model_name}'"
            )

        return compatible_algos[0]

    @staticmethod
    def _check_availability(
        qpu: str,
        resources: list[Resource],
    ) -> Resource:
        matching = [res for res in resources if res.name == qpu]

        if not matching:
            raise LookupError(f"Hardware '{qpu}' not found in provider resources")
        if len(matching) > 1:
            raise ValueError(
                f"Multiple resources found for '{qpu}'. Please adjust filters."
            )
        return matching[0]

    @staticmethod
    def _get_resources(
        local: bool, provider: WorkflowProviderClient | None
    ) -> list[Resource]:
        if local:
            return LOCAL_RESOURCES.list_quantum_resources()
        if not provider:
            raise ConnectionError("Provider client is required for remote execution")
        return provider.list_quantum_resources()

    @staticmethod
    def _run_algorithm_hash(
        algorithm: Algorithm,
        resource: Resource,
        workflow: WorkflowInfo,
    ) -> WorkflowRun:
        res = run(
            entrypoint_hash=algorithm.hash,
            allowed_qpus=[resource.name],
            local_only=True,
        )
        return WorkflowRun(workflow, version=algorithm.version, result=res)

    @staticmethod
    def _run_algorithm_source(
        algorithm: Algorithm, resource: Resource, workflow: WorkflowInfo
    ) -> WorkflowRun:
        algo_source = create_source(algorithm.func(workflow.config))
        header = textwrap.dedent("""\
            from qall import task, workflow
            import qiskit

        """)
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py") as file:
            file.write(header + algo_source)
            file.flush()

            res = run(
                entrypoint_file=file.name,
                local_only=True,
                allowed_qpus=[resource.name],
            )
        return WorkflowRun(workflow, version=algorithm.version, result=res)

    @staticmethod
    def _check_algo_compatibility(algorithm: Algorithm, q_spec: QpuSpec) -> bool:
        """Check if algorithm constraints are satisfied by the hardware specification."""
        if algorithm.hash is None:
            return True

        constraints: dict[str, int | float] = {}

        def collect_constraints(node_hash: str) -> None:
            task = DISK.get_node_from_local(node_hash)
            for key, val in task.resources.quantum.to_dict().items():
                if key not in constraints:
                    constraints[key] = val
                elif key.startswith("max"):
                    constraints[key] = min(constraints[key], val)
                elif key.startswith("min"):
                    constraints[key] = max(constraints[key], val)

            for child_hash in task.children.values():
                collect_constraints(child_hash)

        collect_constraints(algorithm.hash)

        for key, limit in constraints.items():
            spec_val = getattr(q_spec, key, None)
            if spec_val is None:
                continue
            if key.startswith("max") and spec_val > limit:
                return False
            if key.startswith("min") and spec_val < limit:
                return False

        return True
