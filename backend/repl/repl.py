from db.engine import Database
from db.parser import parser
from db.executor import Executor

db = Database()

#projects table
projects = db.create_table(
    name="projects",
    columns=["id", "name"],
    primary_key="id"
)

projects.create_index("id")
projects.create_index("name")

#tasks table
tasks = db.create_table(
    name="tasks",
    columns=["id", "title", "status", "project_id"],
    primary_key="id"
)
tasks.create_index("status")
tasks.create_index("project_id")

executor = Executor(db)

while True:
    sql = input("MiniDB > ")
    if sql.lower() in ("exit", "quit"):
        break
    try:
        tree = parser.parse(sql)
        result = executor.execute(tree)
        print(result)
    except Exception as e:
        print("Error:", e)