# lexer.py

import ply.lex as lex

# Lista de tokens
tokens = (
    'FOR', 'INT', 'ID', 'NUMBER',
    'PLUSPLUS', 'LE', 'EQUALS', 'SEMICOLON',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE'
)

# Palabras reservadas
reserved = {
    'for': 'FOR',
    'int': 'INT'
}

# Expresiones regulares para tokens simples
t_PLUSPLUS = r'\+\+'
t_LE = r'<='
t_EQUALS = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Regla para manejar ID (identificadores y palabras reservadas)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Regla para manejar números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()