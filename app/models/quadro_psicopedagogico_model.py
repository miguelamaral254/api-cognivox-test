from app import db

class QuadroPsicopedagogico(db.Model):
    __tablename__ = 'quadro_psicopedagogico'
    id = db.Column(db.Integer, primary_key=True)
    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id'))
    parecer_psicologico_id = db.Column(db.Integer, db.ForeignKey('parecer_psicologico.id'))

    # Relações
    ator = db.relationship('Ator', backref='quadros_psicopedagogicos')
    parecer_psicologico = db.relationship('ParecerPsicologico', backref='quadros_psicopedagogicos')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}