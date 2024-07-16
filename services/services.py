from flask import jsonify, request
from config.mongodb import mongo
import bcrypt

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
    print(databases)
    return jsonify({'databases':databases})

def createDatabase():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'message': 'Es necesario el nombre para la base de datos'}), 400
    
    nameDatabase = data.get('name')
    client = mongo.cx

    if nameDatabase in client.list_database_names():
        return jsonify({'message': 'La base de datos ya existe'})
    
    client.db.create_collection('')


    # if nameDatabase in mongo.db.list_collection_names


    


def encriptpass(password):
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    encriptpass = bcrypt.hashpw(pwd, salt)
    return encriptpass
