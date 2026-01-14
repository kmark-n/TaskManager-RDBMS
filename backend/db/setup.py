from db.engine import Database
from db.executor import Executor

def setup_database():
    db = Database()
    
    # Initialize Tables
    db.create_table(
        name="projects",
        columns=["id", "name"],
        primary_key="id"
    )
    
    db.create_table(
        name="tasks",
        columns=["id", "title", "status", "project_id"],
        primary_key="id"
    )
    
    # Initialize Indexes
    db.get_table("tasks").create_index("status")
    db.get_table("tasks").create_index("project_id")

    executor = Executor(db)
    return db, executor