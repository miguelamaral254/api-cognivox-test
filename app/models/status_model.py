from app import db

class Status(db.Model):
    __tablename__ = 'status'
    codigo = db.Column(db.Integer, primary_key=True) 
    descricao = db.Column(db.String(255))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}