import json
from yardstiq.object import Algorithm, Module
from . import cursor


def register_algo(algorithm: Algorithm, hash: str):

    cursor.execute(
        "INSERT INTO algorithms (problem, version, hash) VALUES (?, ?, ?)",
        (algorithm.problem, algorithm.version, hash),
    )
    cursor.connection.commit()


def register_module(module: Module, hahs: str):

    tags = json.dumps(module.tags)
    cursor.execute(
        "INSERT INTO modules (name, version, hash, tags) VALUES (?, ?, ?, ?)",
        (module.name, module.version, hash, tags),
    )
    cursor.connection.commit()


def clear_algo():
    cursor.execute("DELETE FROM algorithms")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='algorithms'")
    cursor.connection.commit()


def clear_module():
    cursor.execute("DELETE FROM modules")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='modules'")
    cursor.connection.commit()


def delete_algo(algo_id: int) -> bool:
    cursor.execute("DELETE FROM algorithms WHERE id = ?", (algo_id,))
    cursor.connection.commit()
    return cursor.rowcount > 0


def delete_module(module_id: int) -> bool:
    cursor.execute("DELETE FROM modules WHERE id = ?", (module_id))
    cursor.connection.commit()
    return cursor.rowcount > 0
