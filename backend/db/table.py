from db.index import HashIndex

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
        # 1. PRIMARY KEY HANDLING
        if self.primary_key not in row or row[self.primary_key] is None or row[self.primary_key] == 0:
            row[self.primary_key] = self.next_id
        
        pk = row[self.primary_key]

        # Sync counter
        if isinstance(pk, int) and pk >= self.next_id:
            self.next_id = pk + 1

        if pk in self.rows and pk != 0:
            raise ValueError(f"Primary key violation: ID {pk} already exists in {self.name}")

        # 2. DATA INTEGRITY (Fill missing columns with None/NULL)
        for col in self.columns:
            if col not in row:
                row[col] = None

        # 3. SAVE DATA
        self.rows[pk] = row

        # 4. INDEX UPDATE (With Null Safety)
        for col, index in self.indexes.items():
            if col in row:
                val = row[col]
                # CRITICAL: We don't usually index NULL values in simple HashIndexes
                # to avoid key errors or collision issues
                if val is not None:
                    index.insert(val, pk)

        # 5. EMIT EVENT
        self.emitter.emit("ROW_INSERTED", {
            "table": self.name,
            "row": row
        })
        
        print(f"DEBUG: Table '{self.name}' inserted row. Total count: {len(self.rows)}")
        return row

    def update(self, pk, updates):
        if pk not in self.rows:
            raise ValueError(f"Record with ID {pk} not found")
            
        row = self.rows[pk]

        for col, val in updates.items():
            if col in self.indexes:
                # Null-safe index update
                old_val = row[col]
                if old_val is not None:
                    self.indexes[col].delete(old_val, pk)
                if val is not None:
                    self.indexes[col].insert(val, pk)
            row[col] = val

        self.emitter.emit("ROW_UPDATED", {
            "table": self.name,
            "pk": pk,
            "updates": updates
        })
        return row

    def scan(self):
        self.emitter.emit("TABLE_SCAN", {"table": self.name})
        # Use copy() to prevent React from accidentally mutating the engine's memory
        return [row.copy() for row in self.rows.values()]

    def index_lookup(self, column, value):
        if column not in self.indexes:
            raise ValueError(f"No index on column: {column}")
            
        self.emitter.emit("INDEX_LOOKUP", {
            "table": self.name,
            "column": column,
            "value": value
        })
        ids = self.indexes[column].lookup(value)
        return [self.rows[i] for i in ids]
