from fastapi import FastAPI
from db.engine import Database
from db.parser import parser
from db.executor import Executor

app = FastAPI()

db = Database()
projects = db.create_table(
    name="projects",
    columns=["id", "name"],
    primary_key="id"
)
tasks = db.create_table(
    name="tasks",
    columns=["id", "title", "status", "project_id"],
    primary_key="id"
)
tasks.create_index("status")
tasks.create_index("project_id")

executor = Executor(db)

@app.post("/query")
def run_query(sql: str):
    tree = parser.parse(sql)
    result = executor.execute(tree)
    events = db.emitter.drain()
    return {
        "result": result,
        "events": events
    }
