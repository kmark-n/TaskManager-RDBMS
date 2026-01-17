from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api")
# Initialized in main file
db = None
executor = None
parser = None

def tree_to_dict(tree):
    """Converts the Lark Tree into a JSON-friendly format for the AST Viewer"""
    from lark import Tree
    if isinstance(tree, Tree):
        return {
            "node": str(tree.data),
            "children": [tree_to_dict(c) for c in tree.children]
        }
    return str(tree)

def execute_with_meta(sql: str):
    """Helper to run SQL and return data + engine metadata"""
    try:
        tree = parser.parse(sql)
        result = executor.execute(tree)
        events = db.emitter.drain()
        return {
            "result": result,
            "events": events,
            "ast": tree_to_dict(tree),
            "query": sql
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- ROUTES ---

@router.get("/tasks")
def get_tasks(status: Optional[str] = None, join: bool = False):
    if join:
        sql = "SELECT tasks.id, tasks.title, tasks.status, projects.name FROM tasks JOIN projects ON tasks.project_id = projects.id"
    elif status and status != "All":
        sql = f"SELECT * FROM tasks WHERE status = {status}"
    else:
        sql = "SELECT * FROM tasks"
    return execute_with_meta(sql)

@router.post("/tasks")
def add_task(task: dict):
    # Manual ID strategy for your demo
    sql = (
        f"INSERT INTO tasks VALUES ({task['id']}, '{task['title']}', "
        f"{task['status']}, {task['project_id']})"
    )
    return execute_with_meta(sql)

@router.post("/projects")
def add_project(project: dict):
    sql = f"INSERT INTO projects VALUES ('{project['name']}')"
    return execute_with_meta(sql)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    sql = f"DELETE FROM tasks WHERE id = {task_id}"
    return execute_with_meta(sql)

@router.post("/query")
def custom_query(payload: dict):
    """Endpoint for the raw SQL console in your UI"""
    return execute_with_meta(payload["sql"])

