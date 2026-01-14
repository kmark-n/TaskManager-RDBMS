class HashIndex:
    def __init__(self, column: str, unique: bool = False):
        self.column = column
        self.unique = unique
        self.map = {}

    def insert(self, value, row_id):
        if self.unique and value in self.map:
            raise ValueError("Unique constraint violation")

        self.map.setdefault(value, []).append(row_id)

    def delete(self, value, row_id):
        if value in self.map:
            self.map[value].remove(row_id)
            if not self.map[value]:
                del self.map[value]

    def lookup(self, value):
        return self.map.get(value, [])
