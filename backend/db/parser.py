from lark import Lark

sql_grammar = """
?start: insert | select | update | delete

insert: "INSERT" "INTO" NAME "VALUES" "(" values ")"
select: "SELECT" columns "FROM" NAME join? where_clause?
update: "UPDATE" NAME "SET" assignments where_clause?
delete: "DELETE" "FROM" NAME where_clause

columns: "*" | NAME ("," NAME)*

// JOIN logic
join: "JOIN" NAME "ON" col_name "=" col_name
col_name: NAME "." NAME | NAME

// Core Data Structures
values: value ("," value)*
assignments: assignment ("," assignment)*
assignment: NAME "=" value
where_clause: "WHERE" NAME "=" value

value: SIGNED_NUMBER -> number
     | STRING -> string
     | "NULL" -> null

// Tokens
STRING: /'[^']*'/ | /"[^"]*"/
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""

parser = Lark(sql_grammar)
