class Table:
    def __init__(self, name, columns, primary_key, emitter):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.rows = {}
        self.next_id = 1
        self.indexes = {}
        self.emitter = emitter

        # Primary key index
        self.indexes[primary_key] = HashIndex(primary_key, unique=True)

    def create_index(self, column, unique=False):
        self.indexes[column] = HashIndex(column, unique)

    def insert(self, row):
        pk = row[self.primary_key]
        if pk in self.rows:
            raise ValueError("Primary key violation")

        self.rows[pk] = row

        for col, index in self.indexes.items():
            index.insert(row[col], pk)

        self.emitter.emit("ROW_INSERTED", {
            "table": self.name,
            "row": row
        })

    def update(self, pk, updates):
        row = self.rows[pk]

        for col, val in updates.items():
            if col in self.indexes:
                self.indexes[col].delete(row[col], pk)
                self.indexes[col].insert(val, pk)
            row[col] = val

        self.emitter.emit("ROW_UPDATED", {
            "table": self.name,
            "pk": pk,
            "updates": updates
        })

    def scan(self):
        self.emitter.emit("TABLE_SCAN", {"table": self.name})
        return list(self.rows.values())

    def index_lookup(self, column, value):
        self.emitter.emit("INDEX_LOOKUP", {
            "table": self.name,
            "column": column,
            "value": value
        })
        ids = self.indexes[column].lookup(value)
        return [self.rows[i] for i in ids]
