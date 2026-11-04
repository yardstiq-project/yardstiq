from yardstiq.sdk.engine import engine
from yardstiq.sdk.algorithm import algorithm
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
from yardstiq.sdk.algorithm import AlgorithmRegistry

@engine("quark")
def quark_engine(workflow: WorkflowInfo) -> WorkflowRun:
    """"""

    algorithm = AlgorithmRegistry[workflow.instance.problem](workflow.instance.dataset, workflow.config)
    algorithm_version = AlgorithmRegistry.get_algorithm_version(workflow.instance.problem)
    flow = [workflow]



    for f in algorithm:
        if f.preprocess is not None:
            flow.append(f.preprocess(flow[-1]))
        else:
            flow.append(f(flow[-1]))

    for f in reversed(algorithm):
        if f.postprocess is not None:
            flow.append(f.postprocess(flow[-1]))
        else:
            flow.append(f(flow[-1]))

    return WorkflowRun(workflow, flow, algorithm_version, flow[-1])