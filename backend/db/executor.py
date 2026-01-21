from lark import Tree, Token

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
        if stmt == "delete":
            return self._delete(tree)

    def _get_value(self, val_node):
        """Helper to extract raw Python values from Lark nodes."""
        if not val_node or not isinstance(val_node, Tree):
            # If it's already a Token or raw value
            return str(val_node).strip("'").strip('"')

        inner_val = val_node.children[0]
        
        if val_node.data == "number":
            try:
                return int(inner_val)
            except ValueError:
                return float(inner_val)
                
        if val_node.data == "string":
            return str(inner_val).strip("'").strip('"')

        raw_str = str(inner_val)
        if raw_str.upper() == "NULL":
            return None
            
        return raw_str

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

    def _update(self, tree):
        """
        Handles: UPDATE tasks SET title = 'New', status = 'Done' WHERE id = 1
        """
        table_name = str(tree.children[0].value).lower()
        table = self.db.get_table(table_name)
        
        # 1. Extract ALL assignments (SET col=val, col2=val2)
        updates = {}
        # In most grammars, the assignments node is a child Tree
        assign_node = next(tree.find_data("assignments"))
        for item in assign_node.children:
            # item is usually an 'assignment' tree: [column_name, value]
            col = str(item.children[0].value)
            val = self._get_value(item.children[1])
            updates[col] = val

        # 2. Extract WHERE clause
        where_node = next(tree.find_data("where_clause"))
        where_col = str(where_node.children[0].value)
        where_val = self._get_value(where_node.children[1])

        # 3. Apply updates
        rows_to_update = table.index_lookup(where_col, where_val)
        for r in rows_to_update:
            pk_val = r[table.primary_key]
            table.update(pk_val, updates)

        return {"status": "ok", "updated_count": len(rows_to_update)}

    def _delete(self, tree):
        """
        Handles: DELETE FROM tasks WHERE id = 1
        """
        table_name = str(tree.children[0].value).lower()
        table = self.db.get_table(table_name)

        # Extract WHERE clause
        where_node = next(tree.find_data("where_clause"))
        where_col = str(where_node.children[0].value)
        where_val = self._get_value(where_node.children[1])

        # Find rows
        rows_to_delete = table.index_lookup(where_col, where_val)
        
        for r in rows_to_delete:
            pk_val = r[table.primary_key]
            # Remove from main storage
            if pk_val in table.rows:
                del table.rows[pk_val]
                
                # IMPORTANT: Remove from all indexes too
                for col_name, index in table.indexes.items():
                    val_in_col = r.get(col_name)
                    if val_in_col is not None:
                        index.delete(val_in_col, pk_val)

        # Emit event for real-time UI
        table.emitter.emit("ROWS_DELETED", {
            "table": table_name,
            "count": len(rows_to_delete)
        })

        return {"status": "ok", "deleted_count": len(rows_to_delete)}
