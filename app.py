from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os 


from config.mongodb import mongo
from routes.routes import routes_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)