from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
    }
}

api = Api(
    version='1.0',
    title='API Cognivox',
    description='APIs para o módulo Ator',
    authorizations=authorizations,
    security='Bearer Auth'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    from app.controllers.ator_controller import ator_ns
    from app.controllers.auth_controller import auth_ns

    api.add_namespace(ator_ns, path='/api/ator')
    api.add_namespace(auth_ns, path='/api/auth')

    with app.app_context():
        db.create_all()

    return app