from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os 

from config.mongodb import mongo
from routes.routes import routes_bp

load_dotenv()
print("MONGO_URI:", os.getenv('MONGO_URI'))

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

app.register_blueprint(routes_bp)
@app.route('/test')
def test():
    try:
        db = mongo.db
        return 'Conexión a MongoDB exitosa'
    except Exception as e:
        return f'Error de conexión: {e}'

if __name__ == '__main__':
    app.run(debug=True)