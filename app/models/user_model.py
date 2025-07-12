from app import db

class Usuario(db.Model):
    __tablename__ = 'usuario1' 
    codigo = db.Column(db.Integer, primary_key=True) 
    usuario = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cod_empresa = db.Column(db.Integer)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    cod_status = db.Column(db.Integer)
    cod_grupo_usuario = db.Column(db.Integer)
    cod_nivel = db.Column(db.Integer)
    primeiro_acesso = db.Column(db.Integer)
    erros_login = db.Column(db.Integer)
    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id'), unique=True, nullable=False)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SegProdCognvoxUsuario(db.Model):
    __tablename__ = 'seg_prod_cognvox_usuario1'
    id = db.Column(db.Integer, primary_key=True) 
    usuario = db.Column(db.String(255))
    senha = db.Column(db.String(255))
    cod_status = db.Column(db.Integer)
    cod_ordenacao = db.Column(db.Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}