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
    'ID',  # Token para identificadores
)

# Expresiones regulares para tokens simples
t_FOR = r'\b(for|For|fOr|foR|FOr|fOR|FOR)\b'
t_IF = r'\b(if|If|iF|IF|iFi|Ifi|IFi|IfI)\b'
t_DO = r'\b(do|Do|dO|DO|Od|oD|OD|DO)\b'
t_WHILE = r'\b(while|While|whilE|whiLe|whilE|wHile|WHile|WHILe)\b'
t_ELSE = r'\b(else|Else|elsE|elSe|eLse|ELse|ElSe|ELSE)\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'# Identificadores (variables)

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
            'COMMA': '<Coma>',
            'ID': '<Identificador>',
        }
        symbol = token_descriptions.get(tok.type, tok.type)
        # Crear la cadena de salida en el formato deseado
        #token_info = f"Línea {tok.lineno}\t\tSimbolo\n{symbol}\t\t\t{tok.value}\n"
        token_info = {
            'linea': tok.lineno,
            'simbolo': symbol,
            'valor': tok.value,
        }
        tokens.append(token_info)
    return tokens


# Vista de Django
def home(request):
    tokens = None
    
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')  # Obtener el archivo si se cargó uno
        codigo = request.POST.get('codigo', '')  # Obtener el código del formulario
        
        if archivo:  # Si se cargó un archivo, leer su contenido
            codigo = archivo.read().decode('utf-8')
        
        tokens = analizar_codigo(codigo)  # Analizar el código
        
    return render(request, 'static/index.html', {'tokens': tokens})
