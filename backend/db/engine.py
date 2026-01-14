from db.table import Table
from events.emitter import EventEmitter

class Database:
    def __init__(self):
        self.tables = {}
        self.emitter = EventEmitter()

    def create_table(self, name, columns, primary_key):
        table = Table(name, columns, primary_key, self.emitter)
        self.tables[name] = table
        return table
    
    def get_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Table '{name}' not found.")
        return self.tables[name]

    def table(self, name):
        return self.get_table(name)
