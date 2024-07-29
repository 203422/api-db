from flask import Blueprint
from services.services import login, register, listDatabases, createDatabase, createCollection, insertDocument, getDocuments, updateDocument, deleteDocument, deleteCollection
routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/')
def index():
    print('PROBANDO')
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

@routes_bp.route('/create/database', methods=['POST'])
def create_databases_route():
    return createDatabase()

@routes_bp.route('/create/collection', methods=['POST'])
def create_collection_route():
    return createCollection()

@routes_bp.route('/create/document', methods=['POST'])
def create_document_route():
    return insertDocument()

@routes_bp.route('/get/documents', methods=['POST'])
def get_documents_route():
    return getDocuments()

@routes_bp.route('/update/document', methods=['PUT'])
def update_documents_route():
    return updateDocument()

@routes_bp.route('/delete/document', methods=['DELETE'])
def delete_document_route():
    return deleteDocument()

@routes_bp.route('/delete/collection', methods=['DELETE'])
def delete_collection_route():
    return deleteCollection()
