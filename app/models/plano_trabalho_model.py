from app import db
from datetime import date

class PlanoTrabalho(db.Model):
    __tablename__ = 'plano_trabalho'
    id = db.Column(db.Integer, primary_key=True)
    ator_di_id = db.Column(db.Integer, db.ForeignKey('ator.id'))
    data_inicial_interacao = db.Column(db.Date)
    ator_interacional_id = db.Column(db.Integer, db.ForeignKey('ator.id'))
    ator_professor_id = db.Column(db.Integer, db.ForeignKey('ator.id'))
    ator_psicologo_id = db.Column(db.Integer, db.ForeignKey('ator.id'))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}