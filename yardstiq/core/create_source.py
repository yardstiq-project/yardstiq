from yardstiq.object.module import Module
import inspect


def create_task(
    modules: list[Module],
):

    func_defs = []

    for module in modules:
        raw, _ = inspect.getsourcelines(module.function)
        clean_lines = [line for line in raw if not line.strip().startswith("@module")]
        source = "".join(clean_lines)

        qall_args = ", ".join(
            f"{cle} = {repr(valeur)}" for cle, valeur in module.qall_args.items()
        )
        func_defs.append(f"@task({qall_args})\n{source}")

    res = "\n".join(func_defs) + "\n\n"
    return res


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
        raw, _ = inspect.getsourcelines(module.function)
        clean_lines = [line for line in raw if not line.strip().startswith("@module")]
        source = "".join(clean_lines)

        qall_args = ", ".join(
            f"{cle} = {repr(valeur)}" for cle, valeur in module.qall_args.items()
        )
        func_defs.append(f"@task({qall_args})\n{source}")

        func_name = module.name
        core_lines.append(f"    res = {func_name}(res)")

    res = "\n".join(func_defs) + "\n\n" + "\n".join(core_lines) + "\n"

    return res
