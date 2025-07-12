from app import db

class AtorVinculo(db.Model):
    __tablename__ = 'ator_vinculo_di'
    id = db.Column(db.Integer, primary_key=True)
    ator_id = db.Column(db.Integer, db.ForeignKey('ator.id')) 
    ator_di_id = db.Column(db.Integer, db.ForeignKey('ator.id')) 
    tipo_vinculo_id = db.Column(db.Integer, db.ForeignKey('tipo_vinculo.id'))
    tipo_vinculo = db.relationship('TipoVinculo', backref='vinculos_ator')
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}