from flask import jsonify, request
from config.mongodb import mongo
import bcrypt
from bson.objectid import ObjectId
from analyzer.analizer import parser, lexer, generateTokens

def login():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Todos los campos son requeridos'}), 400
    
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    db = mongo.cx['usersproject']
    user = db.users.find_one({'username': username})
    
    if user and bcrypt.checkpw(password, user['password']):
        return jsonify({'message': 'Sesión iniciada'}), 200
    else:
        return jsonify({'error': 'Nombre de usuario o contraseña incorrectos'}), 401

def register():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Todos los campos son requeridos'}), 400
    
    username = data.get('username')
    password = data.get('password')

    db = mongo.cx['usersproject']
    
    if db.users.find_one({'username': username}):
        return jsonify({'message': 'El usuario ya existe'}), 400
    
    hashed_password = encriptpass(password)
    db.users.insert_one({
        'username': username,
        'password': hashed_password
    })
    
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

def listDatabases():
    client = mongo.cx
    databases = client.list_database_names()
    return jsonify({'databases':databases})

def createDatabase():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia'}), 400

    statement = data.get('statement')

    try:
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}'}), 400

    if not result:
        return jsonify({'message': 'Sentencia inválida'}), 400

    nameDatabase = result['db_name']
    collectionName = result['collection_name']

    client = mongo.cx

    if nameDatabase in client.list_database_names():
        return jsonify({'message': 'La base de datos ya existe'}), 400

    db = client[nameDatabase]
    db.create_collection(collectionName)

    return jsonify({'message': f'Base de datos "{nameDatabase}" y colección "{collectionName}" creadas exitosamente', 'tokens':tokens, 'tokens_count':token_count}), 201
  
def createCollection():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia', 'tokens': [], 'tokens_count': {}}), 400

    statement = data.get('statement')

    try:
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}', 'tokens': [], 'tokens_count': {}}), 400
    
    if not result:
        return jsonify({'message': 'Sentencia inválida', 'tokens': [], 'tokens_count': {}}), 400 
    
    nameDatabase = result['db_name']
    collectionName = result['collection_name']

    client = mongo.cx

    if nameDatabase not in client.list_database_names():
        return jsonify({'message': 'La base de datos no existe', 'tokens': [], 'tokens_count': {}})
    
    db = client[nameDatabase]

    if collectionName in db.list_collection_names():
        return jsonify({'message': 'La colección ya existe', 'tokens': [], 'tokens_count': {}})

    db.create_collection(collectionName)

    if collectionName in db.list_collection_names():
        return jsonify({'message': f'La colección "{collectionName}"  se ha creado exitosamente.', 'tokens':tokens, 'tokens_count':token_count}) 
    else:
        return jsonify({'message': 'Hubo un problema al crear la coleccion', 'tokens': [], 'tokens_count': {}}), 500

def insertDocument():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia', 'tokens': [], 'tokens_count': {}}), 400

    statement = data.get('statement')

    try:
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}', 'tokens': [], 'tokens_count': {}}), 400

    if not result:
        print(result)
        return jsonify({'message': 'Sentencia inválida', 'tokens': [], 'tokens_count': {}}), 400

    if result['type'] != 'insert_document':
        return jsonify({'message': 'Tipo de sentencia inválida para esta operación', 'tokens': [], 'tokens_count': {}}), 400

    db_name = result['db_name']
    collection_name = result['collection_name']
    document = result['document']
    client = mongo.cx

    db = client[db_name]

    if db_name not in client.list_database_names():
        return jsonify({'message': f'La base de datos "{db_name}" no existe', 'tokens': [], 'tokens_count': {}}), 400
    
    if collection_name not in db.list_collection_names():
        return jsonify({'message': f'La colección "{collection_name}" no existe en la base de datos "{db_name}"', 'tokens': [], 'tokens_count': {}}), 400

    if not isinstance(document, dict):
        return jsonify({'message': 'El documento no tiene la estructura adecuada', 'tokens': [], 'tokens_count': {}}), 400

    db[collection_name].insert_one(document)

    return jsonify({'message': 'Documento insertado exitosamente', 'tokens':tokens, 'tokens_count':token_count})

def getDocuments():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia', 'tokens': [], 'tokens_count': {}}), 400

    statement = data.get('statement')

    try:
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}', 'tokens': [], 'tokens_count': {}}), 400

    if not result:
        return jsonify({'message': 'Sentencia inválida', 'tokens': [], 'tokens_count': {}}), 400

    if result['type'] != 'get_documents':
        return jsonify({'message': 'Tipo de sentencia inválida para esta operación', 'tokens': [], 'tokens_count': {}}), 400

    db_name = result['db_name']
    collection_name = result['collection_name']
    client = mongo.cx

    db = client[db_name]
    documents = db[collection_name].find()

    result_docs = []
    for doc in documents:
        doc['_id'] = str(doc['_id'])
        result_docs.append(doc)

    return jsonify({'message': result_docs, 'tokens':tokens, 'tokens_count':token_count}) 
 
def updateDocument():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia', 'tokens': [], 'tokens_count': {}}), 400

    statement = data.get('statement')

    try:
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}', 'tokens': [], 'tokens_count': {}}), 400

    if not result:
        return jsonify({'message': 'Sentencia inválida', 'tokens': [], 'tokens_count': {}}), 400

    if result['type'] != 'update_document':
        return jsonify({'message': 'Tipo de sentencia inválida para esta operación', 'tokens': [], 'tokens_count': {}}), 400

    db_name = result['db_name']
    collection_name = result['collection_name']
    query = result['query']
    update = {'$set': result['update']}
    client = mongo.cx

    db = client[db_name]
    result = db[collection_name].update_one(query, update)

    if result.matched_count > 0:
        return jsonify({'message': 'Documento actualizado exitosamente', 'tokens':tokens, 'tokens_count':token_count})
    else:
        return jsonify({'message': 'No se encontró ningún documento que coincida con la consulta', 'tokens': [], 'tokens_count': {}}), 404
    
def deleteDocument():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia', 'tokens': [], 'tokens_count': {}}), 400

    statement = data.get('statement')

    try:
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}', 'tokens': [], 'tokens_count': {}}), 400
    
    if not result:
        return jsonify({'message': 'Sentencia inválida', 'tokens': [], 'tokens_count': {}}), 400
    
    db_name = result['db_name']
    collection_name = result['collection_name']
    query = result['query']
    client = mongo.cx

    db = client[db_name]
    result = db[collection_name].delete_one(query)

    if result.deleted_count > 0:
        return jsonify({'message': 'Documento eliminado exitosamente', 'tokens':tokens, 'tokens_count':token_count})
    else:
        return jsonify({'message': 'No se encontró ningún documento que coincida con la consulta', 'tokens': [], 'tokens_count': {}}), 404
   
def deleteCollection():
    data = request.get_json()

    if not data or not data.get('statement'):
        return jsonify({'message': 'Es necesario proporcionar una sentencia', 'tokens': [], 'tokens_count': {}}), 400

    statement = data.get('statement')

    try:
        
        tokens, token_count = generateTokens(statement)
        result = parser.parse(statement)
    except Exception as e:
        return jsonify({'message': f'Error en la sentencia: {str(e)}', 'tokens': [], 'tokens_count': {}}), 400

    if not result or result['type'] != 'delete_collection':
        return jsonify({'message': 'Sentencia inválida', 'tokens': [], 'tokens_count': {}}), 400

    db_name = result['db_name']
    collection_name = result['collection_name']
    client = mongo.cx

    db = client[db_name]

    if collection_name not in db.list_collection_names():
        return jsonify({'message': f"La colección '{collection_name}' no existe en la base de datos '{db_name}'.", 'tokens': [], 'tokens_count': {}}), 404

    # Eliminar la colección
    db.drop_collection(collection_name)
    
    return jsonify({'message': f"La colección '{collection_name}' se ha eliminado exitosamente de la base de datos '{db_name}'.", 'tokens':tokens, 'tokens_count':token_count})

def encriptpass(password):
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    encriptpass = bcrypt.hashpw(pwd, salt)
    return encriptpass

