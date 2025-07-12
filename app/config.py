import os

# Importa a função load_dotenv para carregar as variáveis do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env. 
# É bom chamar load_dotenv() logo no início do arquivo de configuração
# ou em run.py antes de carregar a configuração.
load_dotenv() 

class Config:
    # Configurações do Banco de Dados
    # 'DATABASE_URL' é lida do .env. Não há fallback hardcoded aqui.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chaves Secretas para Flask e JWT
    # 'SECRET_KEY' e 'JWT_SECRET_KEY' são lidas do .env.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # Configurações de E-mail
    # Todos os valores são lidos do .env.
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # Converte a porta para inteiro, pois os.environ.get retorna string
    MAIL_PORT = int(os.environ.get('MAIL_PORT')) 
    # Para SSL na porta 465, MAIL_USE_TLS deve ser False e MAIL_USE_SSL deve ser True
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') # Geralmente o remetente padrão é o próprio usuário