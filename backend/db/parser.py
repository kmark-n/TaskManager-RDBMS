from lark import Lark

sql_grammar = """
?start: insert | select | update

insert: "INSERT" "INTO" NAME "VALUES" "(" values ")"
select: "SELECT" columns "FROM" NAME  join? where?
update: "UPDATE" NAME "SET" assignment where?
join: "JOIN" NAME "ON" NAME "." NAME "=" NAME "." NAME

columns: "*" | NAME ("," NAME)*
col_name: (NAME ".")? NAME

values: value ("," value)*
assignment: NAME "=" value
where: "WHERE" NAME "=" value

value: SIGNED_NUMBER -> number
     | STRING -> string

STRING: /'[^']*'/ | /"[^"]*"/
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""

parser = Lark(sql_grammar)
