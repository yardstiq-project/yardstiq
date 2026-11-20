import sqlite3
import json
from qall.core import push_workflow_on_registry
from qall.core.registry import WorkflowSpec
from yardstiq.object import module_database, algorithm_database
import importlib
import os
import tempfile
from .create_source import create_task, create_source
import sys

LOCAL_DB = "local_ys.db"

inst = sqlite3.connect(LOCAL_DB)
cursor = inst.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem TEXT NOT NULL,
    version TEXT NOT NULL,
    hash TEXT NOT NULL,
    infos TEXT NOT NULL,
    requirement TEXT NOT NULL

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

    if requirement is None:
        requirement = []

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Impossible de charger le fichier : {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module 
    spec.loader.exec_module(module)    

    algo = algorithm_database[name][-1]
    algo_source = create_source(algo())
    imp = "from qall import task, workflow\n"
    for req in requirement:
        imp += f"import {req}\n"

    imp += "\n"
    source = imp + algo_source
    folder = os.path.dirname(file_path)
    
    with tempfile.NamedTemporaryFile(mode="w+", delete=True, suffix=".py", dir=folder) as file:
        file.write(source)
        file.flush()   

        work = WorkflowSpec(file.name)
        tag, dag = push_workflow_on_registry(
            workflow_spec=work,
            workflow_name=algo.problem,
            local_only=True,
            workflow_version=algo.version,
        )

        infos = json.dumps(algo.info)
        algo_req = json.dumps(algo.requirements)
        
        cursor.execute(
            "INSERT INTO algorithms (problem, version, hash, infos, requirements) VALUES (?, ?, ?, ?, ?)",
            (algo.problem, algo.version, dag.root_hash, infos, algo_req),
        )
        cursor.connection.commit()

def register_module(file_path: str = None, requirement: list[str] = None):

    print("Registering modules")

    if requirement is None:
        requirement = []

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Impossible de charger le fichier : {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    modules = module_database.get_non_local()
    folder = os.path.dirname(file_path)
    
    for module in modules:

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
            tags = json.dumps(module.tags)
            cursor.execute(
                "INSERT INTO modules (name, version, hash, tags) VALUES (?, ?, ?, ?)",
                (module.name, module.version, dag.root_hash, tags),
            )

            cursor.connection.commit()
