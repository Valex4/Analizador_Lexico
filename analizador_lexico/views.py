from django.shortcuts import render
import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens
tokens = (
    'FOR',
    'IF',
    'DO',
    'WHILE',
    'ELSE',
    'LPAREN',
    'RPAREN',
    'LBRACE',  # Llave de apertura
    'RBRACE',  # Llave de cierre
    'ID',  # Token para identificadores
    'NUMBER',
    'SEMI',  # Punto y coma
    'GT',  # Mayor que
    'LT',  # Menor que
    'EQ',  # Igual
    'PLUS',  # Suma
    'DOT',  # Punto
    'STRING',  # Cadenas de texto
)

# Expresiones regulares para tokens simples
t_FOR = r'\bfor\b'
t_IF = r'\bif\b'
t_DO = r'\bdo\b'
t_WHILE = r'\bwhile\b'
t_ELSE = r'\belse\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_GT = r'>'
t_LT = r'<'
t_EQ = r'='
t_PLUS = r'\+'
t_DOT = r'\.'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores (variables)
t_STRING = r'\".*?\"'  # Cadenas de texto entre comillas
t_NUMBER = r'\d+'  # Números

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

# Reglas de gramática para el analizador sintáctico
def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement_block(p):
    '''statement : LBRACE statements RBRACE'''
    p[0] = ('block', p[2])

def p_statement_for(p):
    '''statement : FOR LPAREN declaration SEMI expression SEMI expression RPAREN statement'''
    p[0] = ('for', p[3], p[5], p[7], p[9])

def p_declaration(p):
    '''declaration : ID EQ NUMBER
                   | ID EQ ID'''
    p[0] = ('declaration', p[1], p[3])

def p_statement_expression(p):
    '''statement : expression SEMI'''
    p[0] = ('expression', p[1])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = ('id', p[1])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])

def p_expression_binop(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression
                  | expression PLUS expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_system_print(p):
    '''expression : ID DOT ID DOT ID LPAREN STRING PLUS expression RPAREN
                  | ID DOT ID DOT ID LPAREN STRING RPAREN'''
    if len(p) == 10:
        p[0] = ('print', p[1], p[3], p[5], p[7], p[9])
    else:
        p[0] = ('print', p[1], p[3], p[5], p[7])

# Variable para detectar errores de sintaxis
syntax_error = False
syntax_error_msg = ""

def p_error(p):
    global syntax_error, syntax_error_msg
    syntax_error = True
    if p:
        syntax_error_msg = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}"
    else:
        syntax_error_msg = "Error de sintaxis al final del archivo"

# Construir el parser
parser = yacc.yacc()

def analizar_codigo(codigo):
    global syntax_error, syntax_error_msg
    syntax_error = False
    syntax_error_msg = ""
    lexer.lineno = 1
    lexer.input(codigo)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Mapear el tipo de token a una descripción legible
        token_descriptions = {
            'FOR': '<Reservada For>',
            'IF': '<Reservada If>',
            'DO': '<Reservada Do>',
            'WHILE': '<Reservada While>',
            'ELSE': '<Reservada Else>',
            'LPAREN': '<Parentesis de apertura>',
            'RPAREN': '<Parentesis de cierre>',
            'LBRACE': '<Llave de apertura>',
            'RBRACE': '<Llave de cierre>',
            'SEMI': '<Punto y coma>',
            'GT': '<Mayor que>',
            'LT': '<Menor que>',
            'EQ': '<Igual>',
            'PLUS': '<Suma>',
            'DOT': '<Punto>',
            'ID': '<Identificador>',
            'STRING': '<Cadena>',
            'NUMBER': '<Número>',
        }
        symbol = token_descriptions.get(tok.type, tok.type)
        # Crear la cadena de salida en el formato deseado
        token_info = f"Línea {tok.lineno} Simbolo {symbol} {tok.value}"
        tokens.append(token_info)
    
    # Análisis sintáctico
    parser.parse(codigo, lexer=lexer)
    if syntax_error:
        resultado_sintactico = f"Error sintáctico: {syntax_error_msg}"
    else:
        resultado_sintactico = "Estructura correcta"
    
    return tokens, resultado_sintactico

# Vista de Django
def home(request):
    tokens = None
    resultado_sintactico = None
    
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')  # Obtener el archivo si se cargó uno
        codigo = request.POST.get('codigo', '')  # Obtener el código del formulario
        
        if archivo:  # Si se cargó un archivo, leer su contenido
            codigo = archivo.read().decode('utf-8')
        
        tokens, resultado_sintactico = analizar_codigo(codigo)  # Analizar el código
        
    return render(request, 'static/index.html', {'tokens': tokens, 'resultado_sintactico': resultado_sintactico})
