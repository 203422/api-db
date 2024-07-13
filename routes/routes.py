from flask import Blueprint, jsonify, request

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return 'Probando API'

@routes.route('/login')
def login():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Todos los campos son requeridos'}), 400
    
