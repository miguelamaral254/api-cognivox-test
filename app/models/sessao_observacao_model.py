from app import db

class SessaoObservacao(db.Model):
    __tablename__ = 'sessao_observacao'
    id = db.Column(db.Integer, primary_key=True)
    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id'))
    descricao = db.Column(db.String(255))
    titulo_sessao = db.Column(db.String(255))
    status = db.Column(db.String(50))

    # Relação
    ator = db.relationship('Ator', backref='sessoes_observacao')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}