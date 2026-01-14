from lark import Lark

sql_grammar = """
?start: insert | select | update

insert: "INSERT" "INTO" NAME "VALUES" "(" values ")"
select: "SELECT" columns "FROM" NAME where?
update: "UPDATE" NAME "SET" assignment where?

columns: "*" | NAME ("," NAME)*
values: value ("," value)*
assignment: NAME "=" value
where: "WHERE" NAME "=" value

value: SIGNED_NUMBER -> number
     | ESCAPED_STRING -> string

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

parser = Lark(sql_grammar)
