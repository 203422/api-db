import ply.lex as lex
import ply.yacc as yacc

# Definir palabras reservadas y tokens
reserved = {
    'create': 'CREATE',
    'database': 'DATABASE',
    'with': 'WITH',
    'collection': 'COLLECTION',
    'insert': 'INSERT',
    'into': 'INTO',
    'get': 'GET',
    'documents': 'DOCUMENTS',
    'from': 'FROM',
    'update': 'UPDATE',
    'set': 'SET',
    'where': 'WHERE',
    'delete': 'DELETE'
}

tokens = [
    'IDENTIFIER',
    'LBRACE', 'RBRACE', 'COLON', 'COMMA', 'STRING', 'NUMBER', 'TRUE', 'FALSE', 'NULL'
] + list(reserved.values())

# Reglas de expresiones regulares para tokens simples
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_COMMA = r','

def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # Remover las comillas
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t

# Caracteres ignorados
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definición de la gramática
def p_statement(p):
    '''statement : create_db
                 | create_collection
                 | insert_document
                 | get_documents
                 | update_document
                 | delete_document
                 | delete_collection'''
    p[0] = p[1]

def p_create_db(p):
    'create_db : CREATE DATABASE IDENTIFIER WITH COLLECTION IDENTIFIER'
    p[0] = {'type': 'create_db', 'db_name': p[3], 'collection_name': p[6]}

def p_create_collection(p):
    'create_collection : CREATE COLLECTION IDENTIFIER INTO DATABASE IDENTIFIER'
    p[0] = {'type': 'create_collection', 'collection_name': p[3], 'db_name': p[6]}

def p_insert_document(p):
    'insert_document : INSERT INTO DATABASE IDENTIFIER COLLECTION IDENTIFIER LBRACE document RBRACE'
    p[0] = {'type': 'insert_document', 'db_name': p[4], 'collection_name': p[6], 'document': p[8]}

def p_get_documents(p):
    'get_documents : GET DOCUMENTS FROM DATABASE IDENTIFIER COLLECTION IDENTIFIER'
    p[0] = {'type': 'get_documents', 'db_name': p[5], 'collection_name': p[7]}

def p_update_document(p):
    'update_document : UPDATE DATABASE IDENTIFIER COLLECTION IDENTIFIER SET LBRACE document RBRACE WHERE LBRACE document RBRACE'
    p[0] = {'type': 'update_document', 'db_name': p[3], 'collection_name': p[5], 'update': p[8], 'query': p[12]}

def p_delete_document(p):
    'delete_document : DELETE FROM DATABASE IDENTIFIER COLLECTION IDENTIFIER WHERE LBRACE document RBRACE'
    p[0] = {'type': 'delete_document', 'db_name': p[4], 'collection_name': p[6], 'query': p[9]}

def p_delete_collection(p):
    'delete_collection : DELETE COLLECTION IDENTIFIER FROM DATABASE IDENTIFIER'
    p[0] = {'type': 'delete_collection', 'collection_name': p[3], 'db_name': p[6]}

def p_document(p):
    '''document : STRING COLON value
                | document COMMA STRING COLON value'''
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    else:
        p[1][p[3]] = p[5]
        p[0] = p[1]

def p_value(p):
    '''value : STRING
             | NUMBER
             | TRUE
             | FALSE
             | NULL'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}'")
    else:
        print("Error sintáctico en EOF")

# Construir el parser
parser = yacc.yacc()


def generateTokens(statement):
    tokens = []
    token_count = {'PR': 0, 'ID': 0, 'NUMBER': 0, 'SYM': 0}

    try:

        lexer.input(statement)
        for token in lexer:
            token_type = token.type
            if token_type in reserved.values():
                token_count['PR'] += 1
            elif token_type == 'IDENTIFIER':
                token_count['ID'] += 1
            elif token_type == 'NUMBER':
                token_count['NUMBER'] += 1
            else:
                token_count['SYM'] += 1
            tokens.append({'type': token.type, 'value': token.value, 'lineno':token.lineno, 'lexpos':token.lexpos})

    except SyntaxError as e:
        print(e)

    return tokens, token_count