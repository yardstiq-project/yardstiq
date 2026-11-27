import sqlite3

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
