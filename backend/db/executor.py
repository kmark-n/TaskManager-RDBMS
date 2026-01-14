class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, tree):
        stmt = tree.children[0].data

        if stmt == "insert":
            return self._insert(tree)
        if stmt == "select":
            return self._select(tree)
        if stmt == "update":
            return self._update(tree)

    def _insert(self, tree):
        table = self.db.table(tree.children[0].value)
        values = [v.children[0] for v in tree.children[1].children]
        row = dict(zip(table.columns, values))
        table.insert(row)
        return {"status": "ok"}

    def _select(self, tree):
        table = self.db.table(tree.children[1].value)

        if len(tree.children) == 3:
            col = tree.children[2].children[0].value
            val = tree.children[2].children[1].children[0]
            return table.index_lookup(col, val)

        return table.scan()

    def _update(self, tree):
        table = self.db.table(tree.children[0].value)
        col = tree.children[1].children[0].value
        val = tree.children[1].children[1].children[0]

        where_col = tree.children[2].children[0].value
        where_val = tree.children[2].children[1].children[0]

        rows = table.index_lookup(where_col, where_val)
        for r in rows:
            table.update(r[table.primary_key], {col: val})

        return {"updated": len(rows)}
