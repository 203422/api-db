from flask import Blueprint
from services.services import login, register, listDatabases

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/')
def index():
    return 'Probando API'

@routes_bp.route('/login', methods=['POST'])
def login_router():
    return login()
    
@routes_bp.route('/register', methods=['POST'])
def register_router():
    return register()

@routes_bp.route('/databases', methods=['GET'])
def list_databases_route():
    return listDatabases()