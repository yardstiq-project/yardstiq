# Glossary

## Business objects
- **Problem**: A formal definition of the problem / use case to resolve / high level view 
Example: Max cut, TSP, ground state… it is human readable.
- **Dataset**: A set of raw data dedicated to a Problem
Example: Specific geometry, weighted matrix…
- **Instance**: Combination of 1 Problem + 1 Dataset. It is the object to evaluate.
Example: Max cut with  G_14 nodes or VQE of Lithium
- **Algorithm**: Implementation of one strategy to solve a Problem. Generic for any Instance of this Problem. Specific for type of QPU Resource / compute modality (ie: mapper to hardware)
- **Configuration**: Hyper parameters of an Algorithm (max shot, max duration, max cost, max iteration, max depth, compilation parameters…)

## Boilerplate objects
- **Task** = Atomic unit of compute running over a Resource
- **Resource** = A place to execute a Task
- **Workflow** = Instance + Configuration + Algorithm + Resource assignment per Task
- **ExecutionProvider** = Service capable to provide Resource to run Workflow over it’s Resource
- **Workflow Run** = Execution of a defined Workflow (workspace in aqora hub)
- **Proof** = Validation certificate of quantum works + Versioning/Reproducibility
- **Result** = Raw results of a Task of the WorkflowRun
- **Solution** = Interpreted/Business result. Best extract solution of the WorkflowRun
- **Metrics** = observability data of the WorkflowRun
- **Register** = Service able to store WorkflowRun data
- **Submission** = Record of a WorkflowRun on a Register
