from lark import Tree, Token
from sqlalchemy import table

class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, tree):
        stmt = tree.data 

        if stmt == "insert":
            return self._insert(tree)
        if stmt == "select":
            return self._select(tree)
        if stmt == "update":
            return self._update(tree)

    def _get_value(self, val_node):
        """Helper to extract raw Python values from Lark nodes."""
        # Safety check for empty nodes
        if not val_node or not val_node.children:
            return None

        # Access the raw Token inside the node
        inner_val = val_node.children[0]
        
        # 1. Handle explicit Numeric types (keeps IDs as integers)
        if val_node.data == "number":
            try:
                return int(inner_val)
            except ValueError:
                return float(inner_val)
                
        # 2. Handle String types (cleans up "Build" -> Build)
        if val_node.data == "string":
            return str(inner_val).strip("'").strip('"')

        # 3. Handle NULL/None (Case-insensitive check for the keyword NULL)
        raw_str = str(inner_val)
        if raw_str.upper() == "NULL":
            return None
            
        return raw_str

    def _insert(self, tree):
    # 1. FIXED: Extract the table name from the first child of the insert tree
    # Depending on your grammar, this is usually tree.children[0]
        table_name = str(tree.children[0].value).lower()
        
        print(f"DEBUG: Attempting to insert into table: '{table_name}'")
        
        table = self.db.get_table(table_name)
        if not table:
            print(f"ERROR: Table '{table_name}' not found in database!")
            return {"status": "error", "message": f"Table '{table_name}' not found"}

        # 2. Extract values from the AST
        values_node = next(tree.find_data("values"))
        values = [self._get_value(child) for child in values_node.children]
        print(f"DEBUG: Parsed values from SQL: {values}")

        # 3. Map values to columns
        # If the user didn't provide an ID, we map to everything except the first column (id)
        if len(values) == len(table.columns) - 1:
            row = dict(zip(table.columns[1:], values))
        else:
            row = dict(zip(table.columns, values))
        
        print(f"DEBUG: Final row dictionary created: {row}")

        # 4. Perform the actual insert
        inserted_row = table.insert(row)
        
        # Verify the table size immediately after
        print(f"DEBUG: Table '{table_name}' now contains {len(table.rows)} rows.")

        return {"status": "ok", "row": inserted_row}

    def _select(self, tree):
        # In select: columns is children[0], NAME is children[1]
        left_table_name = tree.children[1].value
        left_table = self.db.get_table(left_table_name)

        results = left_table.scan()
        print(f"--- ENGINE DATA DUMP ({left_table_name}) ---")
        print(f"Raw rows in memory: {results}")

        for child in tree.children:
            if isinstance(child, Tree) and child.data == "join":
                right_table_name = child.children[0].value
                right_table = self.db.get_table(right_table_name)
                
                # Join Logic: Nested Loop
                joined_results = []
                left_key = child.children[2].value # e.g., project_id
                right_key = child.children[4].value # e.g., id
                
                for l_row in results:
                    for r_row in right_table.scan():
                        if l_row[left_key] == r_row[right_key]:
                            # Merge the dictionaries
                            combined = {**l_row, **r_row}
                            joined_results.append(combined)
                results = joined_results
        print(f"DEBUG: Selecting from {left_table_name}, found {len(results)} rows")
        return results

    def _update(self, tree):
        table_name = tree.children[0].value
        table = self.db.get_table(table_name)
        
        # assignment node
        assign_node = tree.children[1]
        col = assign_node.children[0].value
        val = self._get_value(assign_node.children[1])

        # where node
        where_node = tree.children[2]
        where_col = where_node.children[0].value
        where_val = self._get_value(where_node.children[1])

        rows = table.index_lookup(where_col, where_val)
        for r in rows:
            # Assumes r is a dict and we have the PK value
            pk_val = r[table.primary_key]
            table.update(pk_val, {col: val})

        return {"updated": len(rows)}
