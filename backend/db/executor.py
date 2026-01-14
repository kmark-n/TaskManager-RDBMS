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

    def _get_value(self, val_node):
        """Helper to extract raw Python values from Lark nodes."""
        # val_node is likely a Tree with data='number' or 'string'
        inner_val = val_node.children[0] # This is the Token
        
        if val_node.data == "number":
            return int(inner_val)
        if val_node.data == "string":
            return str(inner_val).strip("'").strip('"')
        return str(inner_val)

    def _insert(self, tree):
        # tree.children[0] is the NAME token for the table
        table_name = tree.children[0].value
        table = self.db.get_table(table_name) # Use the method we fixed earlier
        
        # tree.children[1] is the 'values' tree
        values_node = tree.children[1]
        values = [self._get_value(v) for v in values_node.children]
        
        # Zip column names with the processed values
        row = dict(zip(table.columns, values))
        table.insert(row)
        return {"status": "ok", "row": row}

    def _select(self, tree):
        # In select: columns is children[0], NAME is children[1]
        left_table_name = tree.children[1].value
        left_table = self.db.get_table(left_table_name)

        results = left_table.scan()

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
