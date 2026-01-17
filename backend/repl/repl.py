from db.parser import parser
from db.setup import setup_database


db, executor = setup_database()

while True:
    sql = input("MiniDB > ").strip()
    if sql.lower() in ("exit", "quit"):
        break
    try:
        tree = parser.parse(sql)
        result = executor.execute(tree)
        if isinstance(result, list) and len(result) > 0:
            cols = result[0].keys()
            header = " | ".join(cols)
            print("-" * len(header))
            print(header)
            print("-" * len(header))
            for row in result:
                print(" | ".join(str(row.get(c, "")) for c in cols))
            print(f"({len(result)} rows returned)")
        else:
            print("Success:", result)
    except Exception as e:
        print("Error:", e)
