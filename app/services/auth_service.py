from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify, current_app
from functools import wraps
from app.models.user_model import Usuario
from app import db
import base64
import unicodedata

def get_user_group_from_db(user_email):
    if not user_email:
        return None
    
    with current_app.app_context():
        user = Usuario.query.filter_by(email=user_email).first()
        if user:
            return user.cod_grupo_usuario
        return None

def verify_token(user_email, required_permission_type):
    user_group_id = get_user_group_from_db(user_email)

    if user_group_id is None:
        return False

    if required_permission_type == 'read_ator':
        return user_group_id in [1, 3, 10, 13]
    
    elif required_permission_type == 'write_ator':
        return user_group_id == 1
    
    return False

def base64_encode_py(input_string):
    if not isinstance(input_string, str):
        return None
    return base64.b64encode(input_string.encode('utf-8')).decode('utf-8')

def remove_accents_py(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

def send_email_py(to_email, cc_email, from_email, subject, body):
    print(f"Simulando envio de e-mail para: {to_email}")
    print(f"Assunto: {subject}")
    return True

def get_last_id_py(model_class, id_column='id', filter_condition=None):
    try:
        query = db.session.query(db.func.max(getattr(model_class, id_column)))
        if filter_condition is not None:
            query = query.filter(filter_condition)
        last_id = query.scalar()
        return last_id if last_id is not None else 0
    except Exception as e:
        print(f"Erro ao obter último código (via get_last_id_py): {e}")
        return 0

def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_email = get_jwt_identity()
            user_group_id = get_user_group_from_db(current_user_email)

            if user_group_id is None:
                return jsonify({'message': 'Acesso negado: Usuário não autorizado'}), 403

            if isinstance(roles, int):
                if user_group_id != roles:
                    return jsonify({'message': 'Acesso negado: role insuficiente'}), 403
            elif isinstance(roles, list):
                if user_group_id not in roles:
                    return jsonify({'message': 'Acesso negado: role insuficiente'}), 403
            else:
                return jsonify({'message': 'Configuração de role inválida no servidor'}), 500

            return fn(*args, **kwargs)
        return decorator
    return wrapper
