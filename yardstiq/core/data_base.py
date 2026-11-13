import sqlite3
import json
from qall.core import push_workflow_on_registry
from qall.core.registry import WorkflowSpec
from yardstiq.object import module_database, algorithm_database
import importlib
import os
import tempfile
from create_source import create_task
from pathlib import Path

LOCAL_DB = "local_ys.db"

inst = sqlite3.connect(LOCAL_DB)
cursor = inst.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem TEXT NOT NULL,
    version TEXT NOT NULL,
    hash TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    hash TEXT NOT NULL,
    tags TEXT NOT NULL
)
""")

inst.commit()


def register_algo(file_path: str, name: str, requirement: list[str] = None):
    return
    # if requirement is None:
    #     requirement = []

    # importlib.import_module(file_path)

    # algo = algorithm_database[name]

    # work = WorkflowSpec.from_file(file_path)

    # tag, dag = push_workflow_on_registry(
    #     workflow_spec=work,
    # )

    # hash = "123456789"

    # cursor.execute(
    #     "INSERT INTO algorithms (problem, version, hash) VALUES (?, ?, ?)",
    #     ("Tri Rapide", "1.0.0", hash),
    # )
    # return


def register_module(file_path: str = None, requirement: list[str] = None):

    if requirement is None:
        requirement = []

    importlib.import_module(file_path)
    modules = module_database.get_modules_file(file_path)

    folder = os.path.dirname(file_path)

    source = create_task(modules)

    imp = "from qall import task\n"

    for req in requirement:
        imp += f"import {req}\n"

    imp += "\n"

    file_source = imp + source
    for module in modules:
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=True, suffix=".py", dir=folder
        ) as file:
            file.write(file_source)
            file.flush()

            work = WorkflowSpec.from_file(file.name)
            tag, dag = push_workflow_on_registry(
                workflow_spec=work,
                workflow_name=module.name,
                local_only=True,
                workflow_version=module.version,
            )
            tags = json.dumps(module.tags)
            cursor.execute(
                "INSERT INTO modules (name, version, hash, tags) VALUES (?, ?, ?, ?)",
                (module.name, module.version, dag.root_hash, tags),
            )


def register_(file_path: str, names : list | str, type: str, requirements: list[str] = None):
    if requirements is None:
        requirements = []
    if type not in ["algo", "module"]:
        raise ValueError(f"Register received a {type} but only accepts module or algo.")

    path_json = Path(__file__).parent / "list_modules.json"
    try:
        with open(path_json, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    new_elem = {
        "name" : names,
        "type": type,
        "requirements": requirements,
        "path" : file_path
    }
    data.append(new_elem)
    with open(path_json, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

