from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields 

from app.models.user_model import Usuario
from app.services.auth_service import base64_encode_py
from app import db

auth_ns = Namespace('Auth', description='Operações de Autenticação de Usuários')

login_model = auth_ns.model('Login', {
    'usuario': fields.String(required=True, description='Nome de usuário para login'),
    'senha': fields.String(required=True, description='Senha do usuário')
})

@auth_ns.route('/login') 
class UserLogin(Resource):
    @auth_ns.doc('user_login') 
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login bem-sucedido', auth_ns.model('LoginSuccess', {'access_token': fields.String}))
    @auth_ns.response(400, 'Dados de login ausentes')
    @auth_ns.response(401, 'Usuário ou senha inválidos')
    def post(self):
        data = auth_ns.payload 
        usuario_digitado = data.get('usuario')
        senha_digitada = data.get('senha')

        if not usuario_digitado or not senha_digitada:
            auth_ns.abort(400, "Usuário e senha são obrigatórios")

        senha_codificada_digitada = base64_encode_py(senha_digitada)

        user = Usuario.query.filter_by(
            usuario=usuario_digitado,
            senha=senha_codificada_digitada
        ).first()

        if user is None:
            auth_ns.abort(401, "Usuário ou senha inválidos")

        access_token = create_access_token(identity=user.email)
        return {'access_token': access_token}, 200