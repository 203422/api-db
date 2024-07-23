import ply.lex as lex
import ply.yacc as yacc


reserved  = {
    'create' : 'CREATE',
    'database' : 'DATABASE',
    'with' : 'WITH', 
    'collection' : 'COLLECTION', 
}


tokens = [
    'IDENTIFIER',
] + list(reserved.values())


# Reglas de expresiones regulares para los tokens simples
t_CREATE = r'CREATE'
t_DATABASE = r'DATABASE'
t_WITH = r'WITH'
t_COLLECTION = r'COLLECTION'

# Regla para nombres de base de datos y colecciones (alfanuméricos y guiones bajos)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t

# Caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


def p_statement_create_db(t):
    'statement : CREATE DATABASE IDENTIFIER WITH COLLECTION IDENTIFIER'
    t[0] = {'db_name': t[3], 'collection_name': t[6]}

def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}'")
    else:
        print("Error sintáctico en EOF")

lexer = lex.lex()
parser = yacc.yacc()