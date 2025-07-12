from app import db

class Unidade(db.Model):
    __tablename__ = 'unidade'
    id = db.Column(db.Integer, primary_key=True)
    nome_instituicao = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    estado = db.Column(db.String(255))
    logoinstituicao = db.Column(db.String(255)) 

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}