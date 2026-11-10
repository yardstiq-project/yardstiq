# from yardstiq.sdk.engine import engine
# from yardstiq.object import algorithm_database
# from yardstiq.object.workflow import WorkflowRun, WorkflowInfo


# @engine("quark")
# def quark_engine(workflow: WorkflowInfo) -> WorkflowRun:
#     """"""

#     algorithm = algorithm_database[workflow.instance.problem](
#         workflow.instance.dataset, workflow.config
#     )
#     algorithm_version = algorithm_database.get_algorithm_version(
#         workflow.instance.problem
#     )
#     flow = [workflow.instance.dataset]

#     for f in algorithm:
#         if f.preprocess is not None:
#             flow.append(f.preprocess(flow[-1]))
#         else:
#             flow.append(f(flow[-1]))

#     for f in reversed(algorithm):
#         if f.postprocess is not None:
#             flow.append(f.postprocess(flow[-1]))
#         else:
#             flow.append(f(flow[-1]))

#     return WorkflowRun(workflow, flow, algorithm_version, flow[-1])
