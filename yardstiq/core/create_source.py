from yardstiq.object.module import Module
import inspect
import ast
import textwrap


def create_task(modules: list[Module], entrypoint: bool = False):
    func_defs = []
    for module in modules:
        raw_source = inspect.getsource(module.function)
        source = remove_module_decorator(raw_source)

        qall_args = ", ".join(
            f"{cle} = {repr(valeur)}" for cle, valeur in module.qall_args.items()
        )
        if entrypoint:
            qall_args = "entrypoint=True, " + qall_args

        func_defs.append(f"@task({qall_args})\n{source}")

    return "\n".join(func_defs) + "\n\n"


def remove_module_decorator(source: str) -> str:
    dedented = textwrap.dedent(source)
    tree = ast.parse(dedented)

    func_node = tree.body[0]

    if isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        new_decorators = []
        for dec in func_node.decorator_list:
            is_bare_module = isinstance(dec, ast.Name) and dec.id == "module"
            is_call_module = (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Name)
                and dec.func.id == "module"
            )

            if not (is_bare_module or is_call_module):
                new_decorators.append(dec)

        func_node.decorator_list = new_decorators

    return ast.unparse(tree)


def create_workflow(
    modules: list[Module],
):

    core_lines = [
        "@workflow(requirements=['qiskit', 'numpy'])",
        "def dynamique_source():",
        "    res = None",
    ]

    for module in modules:
        func_name = module.name
        core_lines.append(f"    res = {func_name}(res)")

    res = "\n".join(core_lines) + "\n"

    return res


def create_source(
    modules: list[Module],
):
    func_defs = []
    core_lines = [
        "@workflow(requirements=['qiskit', 'numpy'])",
        "def example_source():",
        "    res = None",
    ]

    for module in modules:
        raw_source = inspect.getsource(module.function)
        source = remove_module_decorator(raw_source)

        qall_args = ", ".join(
            f"{cle} = {repr(valeur)}" for cle, valeur in module.qall_args.items()
        )
        func_defs.append(f"@task({qall_args})\n{source}\n")

        func_name = module.name
        core_lines.append(f"    res = {func_name}(res)")

    res = "\n".join(func_defs) + "\n\n" + "\n".join(core_lines) + "\n"

    return res
