from fastapi import FastAPI
from db.setup import setup_database
from db.parser import parser


app = fastAPI()
db, executor = setup_database()


@app.post("/query")
def run_query(sql: str):
    tree = parser.parse(sql)
    result = executor.execute(tree)
    events = db.emitter.drain()
    return {
        "result": result,
        "events": events
    }
