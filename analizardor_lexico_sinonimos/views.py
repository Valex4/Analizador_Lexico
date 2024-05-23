from django.shortcuts import render
import ply.lex as lex

# Definición de tokens
tokens = (
    'WORD',
    'NUMBER',
    'SYMBOL'
)

# Expresiones regulares para tokens simples
t_WORD = r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+'
t_NUMBER = r'\d+'
t_SYMBOL = r'[^\w\s]'

# Diccionario de sinónimos
sinonimos = {
    "fácil": "sencillo",
    "morir": "fallecer",
    "rápido": "veloz",
    "hablar": "conversar",
    "casa": "hogar",
    "feliz": "contento",
    "grande": "enorme",
    "pequeño": "diminuto",
    "decir": "expresar",
    "comenzar": "iniciar",
    "terminar": "finalizar",
    "ver": "observar",
    "venir": "llegar",
    "ir": "marchar",
    "andar": "caminar",
    "escribir": "redactar",
    "dificil": "complicado",
    "comprar": "adquirir",
    "vender": "comercializar",
    "encontrar": "hallar",
    "buscar": "explorar",
    "tomar": "agarrar",
    "trabajar": "laborar",
    "ayudar": "asistir",
    "cambiar": "modificar",
    "escuchar": "oír",
    "pensar": "reflexionar",
    "conocer": "saber",
    "dar": "entregar",
    "comer": "alimentarse",
    "beber": "tomar",
    "mirar": "contemplar",
    "contar": "relatar",
    "recordar": "rememorar",
    "olvidar": "desmemoriar",
    "dormir": "descansar",
    "nacer": "surgir",
    "crecer": "aumentar",
    "vivir": "existir",
    "amar": "querer",
    "odiar": "detestar",
    "dejar": "abandonar",
    "recibir": "obtener",
    "enviar": "remitir",
    "leer": "peruse",
    "romper": "desgarrar",
    "construir": "edificar",
    "destruir": "demoler",
    "abrir": "desplegar",
    "cerrar": "clausurar",
    "ganar": "triunfar",
}

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

sinonimos_inverso = {v: k for k, v in sinonimos.items()}


def obtener_palabra_cambiada(palabra):
    # Verificar si la palabra está en el diccionario original
    if palabra in sinonimos:
        return sinonimos[palabra]
    # Verificar si la palabra está en el diccionario inverso
    elif palabra in sinonimos_inverso:
        return sinonimos_inverso[palabra]
    # Si no está en ninguno, devolver la palabra original
    return palabra


def analizar_codigo(codigo):
    lexer.lineno = 1
    lexer.input(codigo)
    tokens_analizados = []
    resultado = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        token_info = {
            'token': tok.value,
            'tipo': tok.type,
            'NUMBER': tok.type == 'NUMBER',
            'SYMBOL': tok.type == 'SYMBOL',
            'Línea': tok.lineno
        }

        palabra_cambiada = obtener_palabra_cambiada(tok.value)
        token_info['SINONIMO'] = palabra_cambiada if palabra_cambiada != tok.value else ''
        tokens_analizados.append(token_info)

    for token in tokens_analizados:
        resultado.append({
            'entrada': token['token'],
            'resultado': token['SINONIMO'],
            'cambiadas': 'x' if token['SINONIMO'] else '',
            'Números': 'x' if token['NUMBER'] else '',
            'Símbolos': 'x' if token['SYMBOL'] else '',
            'Línea': token['Línea']
        })

    return resultado

# Create your views here.

def home(request):
    resultado = []
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        resultado = analizar_codigo(codigo)
    return render(request, 'static/sinonimos.html', {'resultado': resultado})
