from db.parser import parser
from db.setup import setup_database


db, executor = setup_database()

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