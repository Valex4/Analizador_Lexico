from django.shortcuts import render
import ply.lex as lex


# Definición de tokens
tokens = (
    'FOR',
    'IF',
    'DO',
    'WHILE',
    'ELSE',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'ID',
    'INT',
    'PROGRAMA',
    'READ',
    'END',
    'PRINTF',
    'LIZQ',
    'LDER',
    'PUNTOCOMA',
    'VARIABLE',
    'OPERATOR'
)

# Expresiones regulares para tokens simples
t_FOR = r'\b(for|For|fOr|foR|FOr|fOR|FOR)\b'
t_IF = r'\b(if|If|iF|IF|iFi|Ifi|IFi|IfI)\b'
t_DO = r'\b(do|Do|dO|DO|Od|oD|OD|DO)\b'
t_WHILE = r'\b(while|While|whilE|whiLe|whilE|wHile|WHile|WHILe|WHILE|whiLE)\b'
t_ELSE = r'\b(else|Else|elsE|elSe|eLse|ELse|ElSe|ELSE)\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LIZQ = r'\{'
t_LDER = r'\}'
t_COMMA = r','
t_PUNTOCOMA = r';'
t_OPERATOR = r'[\+\-\*\=]'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_VARIABLE(t):
    r'[abc]'
    return t

def t_PROGRAMA(t):
    r'programa'
    return t

def t_INT(t):
    r'int'
    return t

def t_READ(t):
    r'\b(read)\b'
    return t

def t_END(t):
    r'end'
    return t

def t_PRINTF(t):
    r'printf'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función para capturar errores de token
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

lexer.t_newline = t_newline

def analizar_codigo(codigo):
    lexer.lineno = 1
    lexer.input(codigo)
    tokens_analizados = []
    conteos = {
        'PR': 0,
        'ID': 0,
        'SI': 0,
        'LLI': 0,
        'LLD': 0,
        'PC': 0,
        'COMMA': 0,
        'PIZQ': 0,
        'PDER': 0,
        'VAR': 0,
        'OPERATOR': 0,
        'token': 0
    }
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_info = {
            'token': tok.value,
            'tipo': tok.type,
            'PR': tok.type in ['FOR', 'IF', 'DO', 'WHILE', 'ELSE', 'PROGRAMA', 'INT', 'END', 'READ', 'PRINTF'],
            'ID': tok.type == 'ID',
            'LLI': tok.type == 'LIZQ',
            'PC': tok.type == 'PUNTOCOMA',
            'LLD': tok.type == 'LDER',
            'PIZQ': tok.type == 'LPAREN',
            'PDER': tok.type == 'RPAREN',
            'COMMA': tok.type == 'COMMA',
            'VAR': tok.type == 'VARIABLE' or tok.value in ['a', 'b', 'c'],
            'OPERATOR': tok.type == 'OPERATOR' or tok.value in ['+', '=', '-', '*'],
            'SI': tok.type in ['LPAREN', 'RPAREN', 'COMMA', ]
        }
        
        for key in conteos:
            if token_info[key]:
                conteos[key] += 1
        
        tokens_analizados.append(token_info)

    return tokens_analizados, conteos


# Vista de Django
def home(request):
    tokens_analizados = []
    conteos = {
        'PR': 0,
        'ID': 0,
        'SI': 0,
        'LLI': 0,
        'LLD': 0,
        'PC': 0,
        'COMMA': 0,
        'PIZQ': 0,
        'PDER': 0,
        'VAR': 0,
        'OPERATOR': 0,
        'token': 0
    }
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        tokens_analizados, conteos = analizar_codigo(codigo)
    return render(request, 'static/prueba.html', {'tokens_analizados': tokens_analizados, 'conteos': conteos})



def calcular_total(productos):
    iva = 0.16  # 16% de IVA
    resultados = []

    for nombre_producto, precio in productos:
        iva_monto = precio * iva
        total = precio + iva_monto
        resultado = {
            'nombre': nombre_producto,
            'precio': precio,
            'iva': iva_monto,
            'total': total
        }
        resultados.append(resultado)

    return resultados


def examen(request):
    resultado = []

    if request.method == 'POST':
        productos = []
        for nombre in request.POST.getlist('nombre'):
            precio_str = request.POST.get(f'precio_{len(productos)}')
            if precio_str:
                precio = float(precio_str)
                productos.append((nombre, precio))

        resultado = calcular_total(productos)

    return render(request, 'static/Examen.html', {'resultados': resultado})



 
