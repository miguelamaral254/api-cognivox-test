from app import db
from datetime import datetime

class Ator(db.Model):
    __tablename__ = 'ator'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14))
    ano_sessao = db.Column(db.String(4))
    data_nascimento = db.Column(db.Date)
    data_inicio_intervencao = db.Column(db.Date)
    reg_profissional = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefone_cel = db.Column(db.String(20))
    telefone_fixo = db.Column(db.String(20))
    idioma_id = db.Column(db.Integer)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'))
    profissao_id = db.Column(db.Integer, db.ForeignKey('profissao.id'))
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    hexadecimal_foto = db.Column(db.String(255))
    modalidade_ensino_id = db.Column(db.Integer, db.ForeignKey('modalidade_ensino.id'))
    status = db.Column(db.Integer)
    unidade = db.relationship('Unidade', backref='atores')
    profissao = db.relationship('Profissao', backref='atores')
    modalidade_ensino = db.relationship('ModalidadeEnsino', backref='atores')
    vinculos_di = db.relationship('AtorVinculo', foreign_keys='AtorVinculo.ator_di_id', backref='ator_di', lazy=True)
    vinculos_ator = db.relationship('AtorVinculo', foreign_keys='AtorVinculo.ator_id', backref='ator_vinculado', lazy=True)
    planos_trabalho_di = db.relationship('PlanoTrabalho', foreign_keys='PlanoTrabalho.ator_di_id', backref='ator_plano_di', lazy=True)
    planos_trabalho_interacional = db.relationship('PlanoTrabalho', foreign_keys='PlanoTrabalho.ator_interacional_id', backref='ator_plano_interacional', lazy=True)
    planos_trabalho_professor = db.relationship('PlanoTrabalho', foreign_keys='PlanoTrabalho.ator_professor_id', backref='ator_plano_professor', lazy=True)
    planos_trabalho_psicologo = db.relationship('PlanoTrabalho', foreign_keys='PlanoTrabalho.ator_psicologo_id', backref='ator_plano_psicologo', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'ano_sessao': self.ano_sessao,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'data_inicio_intervencao': self.data_inicio_intervencao.isoformat() if self.data_inicio_intervencao else None,
            'reg_profissional': self.reg_profissional,
            'email': self.email,
            'telefone_cel': self.telefone_cel,
            'telefone_fixo': self.telefone_fixo,
            'idioma_id': self.idioma_id,
            'unidade_id': self.unidade_id,
            'profissao_id': self.profissao_id,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'pais': self.pais,
            'hexadecimal_foto': self.hexadecimal_foto,
            'modalidade_ensino_id': self.modalidade_ensino_id,
            'status': self.status
        }