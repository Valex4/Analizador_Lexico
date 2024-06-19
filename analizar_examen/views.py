from django.shortcuts import render

# Create your views here.
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
    pass

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
    #formato_for_valido = validar_for(codigo)
    formato_for_valido = True

    # Analizador Léxico
    tokens = []
    palabras_reservadas = {'inicio', 'fin', 'proceso', 'si', 'ver', 'cadena'}
    simbolos = {'(', ')', '{', '}', '=', ';', '<=', '++', '<', '>=', '>', '=='}
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
    evaluacion1, evaluacion2, es_valido_semantico = validar_semantica(tokens, codigo)

    return tokens, conteo_tokens, es_valido_sintactico, es_valido_semantico, formato_for_valido, evaluacion1, evaluacion2

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
    variables = {}
    lines = codigo.split(';')
    evaluacion1 = None
    evaluacion2 = None

    for line in lines:
        line = line.strip()
        if line.startswith('si('):
            condition = line[3:-2]
            if '==' in condition:
                left, right = condition.split('==')
                if left.strip() in variables and right.strip() in variables:
                    left_value = variables[left.strip()]
                    right_value = variables[right.strip()]
                    print(f"Evaluando: {left_value} == {right_value}")
                    if left_value == right_value:
                        evaluacion1 = True
                        print("Si se cumplio la evaluacion 1")
                    else:
                        evaluacion1 = False
                        print("evaluacion 1 es falso")
            elif '=' in condition:
                var_name, value = condition.split('=')
                var_name = var_name.strip()
                value = value.strip()
                if var_name in variables:
                    var_value = variables[var_name]
                    print(f"Evaluando: {var_value} = {value}")
                    if var_value == value:
                        evaluacion2 = True
                    else:
                        evaluacion2 = False
        elif line.startswith(('inicio', 'fin', 'proceso', 'ver')):
            if not line.endswith(';'):
                return True, True, False  # Estructura incorrecta para inicio, fin, proceso, ver

    variables_declaradas = set(variables.keys())
    for token in tokens:
        if token[0] == 'ID' and token[1] not in variables_declaradas:
            return True, True, False  # Variable no declarada

    return evaluacion1, evaluacion2, True

def home(request):
    tokens = None
    conteo_tokens = None
    es_valido_sintactico = None
    es_valido_semantico = None
    formato_for_valido = None
    validacion2 = None
    validacion1 = None
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['code']
            tokens, conteo_tokens, es_valido_sintactico, es_valido_semantico, formato_for_valido, validacion1, validacion2 = analizar_codigo(codigo)
    else:
        form = CodeForm()
    return render(request, 'static/examenC2.html', {
        'form': form,
        'tokens': tokens,
        'conteo_tokens': conteo_tokens,
        'es_valido_sintactico': es_valido_sintactico,
        'es_valido_semantico': es_valido_semantico,
        'formato_for_valido': formato_for_valido,
        'validacion1' : validacion1,
        'validacion2': validacion2
    })
