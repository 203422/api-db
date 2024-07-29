import ply.lex as lex
import ply.yacc as yacc

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

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_COMMA = r','

def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1] 
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
    r'[a-zA-Z_À-ÿ][a-zA-Z_0-9À-ÿ]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    return t


t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

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
    'insert_document : INSERT LBRACE document RBRACE INTO DATABASE IDENTIFIER COLLECTION IDENTIFIER'
    p[0] = {'type': 'insert_document', 'document': p[3], 'db_name': p[7], 'collection_name': p[9]}

def p_get_documents(p):
    'get_documents : GET DOCUMENTS FROM DATABASE IDENTIFIER COLLECTION IDENTIFIER'
    p[0] = {'type': 'get_documents', 'db_name': p[5], 'collection_name': p[7]}

def p_update_document(p):
    'update_document : UPDATE LBRACE document RBRACE WHERE LBRACE document RBRACE INTO DATABASE IDENTIFIER COLLECTION IDENTIFIER '
    p[0] = {'type': 'update_document', 'update': p[3], 'query': p[7], 'db_name': p[11], 'collection_name': p[13]}

def p_delete_document(p):
    'delete_document : DELETE LBRACE document RBRACE FROM DATABASE IDENTIFIER COLLECTION IDENTIFIER'
    p[0] = {'type': 'delete_document', 'query': p[3],  'db_name': p[7], 'collection_name': p[9]}

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
        raise SyntaxError(f"Error sintáctico en '{p.value}'")
    else:
        raise SyntaxError("Error sintáctico en EOF")

parser = yacc.yacc()

def generateTokens(statement):
    tokens = []
    token_count = {'PR': 0, 'ID': 0, 'NUMBER': 0, 'STRING': 0, 'BOOL': 0, 'SYM': 0, 'NULL': 0}

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
            elif token_type == 'STRING':
                token_count['STRING'] += 1
            elif token_type == "TRUE" or token_type == "FALSE":
                token_count['BOOL'] += 1
            elif token_type == 'NULL':
                token_count['NULL'] += 1
            else:
                token_count['SYM'] += 1
            tokens.append({'type': token.type, 'value': token.value, 'lineno': token.lineno, 'lexpos': token.lexpos})

    except SyntaxError as e:
        print(e)

    return tokens, token_count