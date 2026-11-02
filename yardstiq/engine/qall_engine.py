from qall import task, workflow
from yardstiq.sdk.engine import engine
from yardstiq.sdk.algorithm import algorithm
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
from yardstiq.sdk.algorithm import AlgorithmRegistry

@engine("qall")
def quall_engine(workflow: WorkflowInfo) -> WorkflowRun:
    """"""

    # uses qall entry point to run workflow

    # get qall workflow
    # run qall workflow

    algorithm = AlgorithmRegistry[workflow.instance.problem](workflow.config)
    version = AlgorithmRegistry.get_algorithm_version(workflow.instance.problem)
    flow = [workflow.data.content]
    
    for module in algorithm:
        flow.append(module.preprocess(flow[-1]))

    for module in reversed(algorithm):
        flow.append(module.postprocess(flow[-1]))

    return WorkflowRun(workflow, flow, version, flow[-1])
