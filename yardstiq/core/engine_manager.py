from yardstiq.object.workflow import Workflow, WorkflowRun



def engine_manager(workflow : Workflow, pipeline : str) -> WorkflowRun:
    """Function that take a workflow and uses a pipeline to run it. 
    Engine manager is just to dispatch the workflow to the pipeline.
    
    
    """
    return WorkflowRun(workflow, "Hello world", 10 )


