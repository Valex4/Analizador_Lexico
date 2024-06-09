import re
from django.shortcuts import render
import ply.yacc as yacc
from .forms import CodeForm

# Lista de tokens
tokens = (
    'PR_FOR',
    'LEFT_PAREN',
    'PR_INT',
    'ID',
    'EQUALS',
    'NUMBER',
    'SEMICOLON',
    'RIGHT_PAREN',
    'LEFT_BRACE',
    'RIGHT_BRACE',
    'PLUS',
    'LESSTHANOREQUALS',
)

# Reglas de gramática
def p_statement(p):
    '''statement : PR_FOR LEFT_PAREN PR_INT ID EQUALS NUMBER SEMICOLON ID LESSTHANOREQUALS NUMBER SEMICOLON ID PLUS PLUS RIGHT_PAREN LEFT_BRACE statement_list RIGHT_BRACE
                 | PR_FOR LEFT_PAREN ID EQUALS NUMBER SEMICOLON ID LESSTHANOREQUALS NUMBER SEMICOLON ID PLUS PLUS RIGHT_PAREN LEFT_BRACE statement_list RIGHT_BRACE
                 | PR_FOR LEFT_PAREN PR_INT ID EQUALS NUMBER SEMICOLON ID LESSTHANOREQUALS NUMBER SEMICOLON ID PLUS PLUS RIGHT_PAREN LEFT_BRACE RIGHT_BRACE
                 | PR_FOR LEFT_PAREN ID EQUALS NUMBER SEMICOLON ID LESSTHANOREQUALS NUMBER SEMICOLON ID PLUS PLUS RIGHT_PAREN LEFT_BRACE RIGHT_BRACE'''
    pass

def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    pass

def p_statement_empty(p):
    '''statement : '''
    pass

def p_error(p):
    print("Error de sintaxis en la entrada!")

# Parser
parser = yacc.yacc()

# Función para validar el formato del for y la declaración de la variable
def validar_for(codigo):
    # Patrón regex para validar el formato del for
    patron_for = r'\bfor\s*\(\s*(int\s+)?\w+\s*=\s*\d+\s*;\s*\w+\s*(<=|<|>=|>)\s*\d+\s*;\s*\w+\s*\+\+\s*\)'
    coincidencia = re.search(patron_for, codigo)

    # Verificar si la variable iteradora está declarada fuera del for
    if not coincidencia:
        patron_variable_fuera = r'\bint\s+\w+\s*;'
        variable_fuera_coincidencia = re.search(patron_variable_fuera, codigo)
        if variable_fuera_coincidencia:
            variable_name = re.search(r'\bint\s+(\w+)\s*;', codigo).group(1)
            patron_for_sin_declarar = rf'\bfor\s*\(\s*{variable_name}\s*=\s*\d+\s*;\s*{variable_name}\s*(<=|<|>=|>)\s*\d+\s*;\s*{variable_name}\s*\+\+\s*\)'
            coincidencia = re.search(patron_for_sin_declarar, codigo)

    return bool(coincidencia)

# Analizador de código
def analizar_codigo(codigo):
    # Validar el formato del for
    formato_for_valido = validar_for(codigo)
    
    # Analizador Léxico
    tokens = []
    palabras_reservadas = {'for', 'int', 'float', 'char', 'double', 'long'}
    simbolos = {'(', ')', '{', '}', '=', ';', '<=', '++', '<', '>=', '>'}
    codigo_dividido = codigo.replace('(', ' ( ').replace(')', ' ) ').replace('{', ' { ').replace('}', ' } ').replace(';', ' ; ').replace('<=', ' <= ').replace('++', ' ++ ').replace('<', ' < ').replace('>=', ' >= ').replace('>', ' > ').split()
    conteo_tokens = {
        'PR': 0,
        'ID': 0,
        'Número': 0,
        'Símbolo': 0,
        'Error': 0
    }
    for palabra in codigo_dividido:
        if palabra in palabras_reservadas:
            tokens.append(('PR', palabra))
            conteo_tokens['PR'] += 1
        elif palabra in simbolos:
            tokens.append(('Símbolo', palabra))
            conteo_tokens['Símbolo'] += 1
        elif palabra.isdigit():
            tokens.append(('Número', palabra))
            conteo_tokens['Número'] += 1
        elif palabra.isidentifier():
            tokens.append(('ID', palabra))
            conteo_tokens['ID'] += 1
        else:
            tokens.append(('Error', palabra))
            conteo_tokens['Error'] += 1

    # Analizador Sintáctico
    es_valido_sintactico = validar_sintaxis(tokens)

    # Analizador Semántico
    es_valido_semantico = validar_semantica(tokens, codigo)

    return tokens, conteo_tokens, es_valido_sintactico, es_valido_semantico, formato_for_valido

def validar_sintaxis(tokens):
    try:
        # Convertir tokens en una cadena de entrada
        entrada = ' '.join([token[1] for token in tokens])
        parser.parse(entrada)
        return True
    except Exception as e:
        print(e)
        return False

def validar_semantica(tokens, codigo):
    variables_declaradas = set()
    dentro_del_for = False
    iter_tokens = iter(tokens)

    # Buscar variables declaradas fuera del for
    patron_variable_fuera = r'\bint\s+(\w+)\s*;'
    for match in re.finditer(patron_variable_fuera, codigo):
        variables_declaradas.add(match.group(1))

    for tipo, token in iter_tokens:
        if tipo == 'PR' and token == 'for':
            dentro_del_for = True
        elif dentro_del_for and tipo == 'PR' and token == 'int':
            siguiente = next(iter_tokens, None)
            if siguiente and siguiente[0] == 'ID':
                variables_declaradas.add(siguiente[1])
        elif tipo == 'ID' and token not in variables_declaradas:
            return False
        elif tipo == 'RIGHT_BRACE':
            dentro_del_for = False
    return True

def home(request):
    tokens = None
    conteo_tokens = None
    es_valido_sintactico = None
    es_valido_semantico = None
    formato_for_valido = None
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['code']
            tokens, conteo_tokens, es_valido_sintactico, es_valido_semantico, formato_for_valido = analizar_codigo(codigo)
    else:
        form = CodeForm()
    return render(request, 'static/index2.html', {
        'form': form,
        'tokens': tokens,
        'conteo_tokens': conteo_tokens,
        'es_valido_sintactico': es_valido_sintactico,
        'es_valido_semantico': es_valido_semantico,
        'formato_for_valido': formato_for_valido,
    })
