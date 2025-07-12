from app import db
from app.models.ator_model import Ator
from app.models.user_model import Usuario, SegProdCognvoxUsuario
from app.models.unidade_model import Unidade
from app.models.modalidade_ensino_model import ModalidadeEnsino
from app.models.profissao_model import Profissao
from app.models.parecer_psicologico_model import ParecerPsicologico
from app.models.quadro_psicopedagogico_model import QuadroPsicopedagogico
from app.models.status_model import Status
from app.models.sessao_observacao_model import SessaoObservacao
from app.models.tipo_vinculo_model import TipoVinculo
from app.models.plano_trabalho_model import PlanoTrabalho
from app.models.ator_vinculo_model import AtorVinculo
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import aliased

class AtorRepository:
    def get_all_atores(self):
        return Ator.query.order_by(Ator.nome).all()

    def get_ator_by_id(self, ator_id):
        return Ator.query.get(ator_id)

    def get_ator_by_email(self, email):
        return Ator.query.filter_by(email=email).first()

    def get_user_by_username(self, username):
        return Usuario.query.filter_by(usuario=username).first()

    def get_ator_by_cpf(self, cpf):
        return Ator.query.filter_by(cpf=cpf).first()

    def add_ator(self, ator):
        db.session.add(ator)

    def add_user(self, user):
        db.session.add(user)

    def add_sec_user(self, sec_user):
        db.session.add(sec_user)

    def add_ator_vinculo(self, ator_vinculo):
        db.session.add(ator_vinculo)

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def flush(self):
        db.session.flush()

    def begin_nested(self):
        return db.session.begin_nested()

    def update_plano_trabalho_by_ator_id(self, ator_id, data):
        PlanoTrabalho.query.filter_by(ator_di_id=ator_id).update(data, synchronize_session=False)

    def get_user_by_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def get_sec_user_by_cod_ordenacao(self, cod_ordenacao):
        return SegProdCognvoxUsuario.query.filter_by(cod_ordenacao=cod_ordenacao).first()

    def count_alunos(self):
        return Ator.query.filter(Ator.profissao_id == 1, Ator.status != 2).count()

    def get_ator_descriptions(self):
        return Ator.query.with_entities(Ator.id, Ator.nome).order_by(Ator.id).all()

    def get_ator_combo_names(self):
        return [a.nome for a in Ator.query.with_entities(Ator.nome).order_by(Ator.nome).all()]

    def get_ator_combo_all(self):
        return Ator.query.with_entities(Ator.id, Ator.nome).filter(Ator.status != 2).order_by(Ator.nome).all()

    def get_ator_year_session(self, ator_id):
        return Ator.query.with_entities(Ator.ano_sessao).filter_by(id=ator_id).first()

    def get_ator_type(self, ator_id):
        return db.session.query(
            Ator.id,
            Ator.nome,
            Profissao.descricao.label('tipo')
        ).outerjoin(Profissao, Profissao.id == Ator.profissao_id)\
        .filter(Ator.status != 2, Ator.id == ator_id).first()

    def get_filtered_actors_for_caderno_atividades(self, query_filters, city_filter):
        ator_query = db.session.query(
            Ator.id,
            Ator.nome,
            func.timestampdiff(func.year, Ator.data_nascimento, func.now()).label('IDADE'),
            Ator.hexadecimal_foto,
            Ator.ano_sessao,
            ModalidadeEnsino.descricao.label('MODALIDADE'),
            Profissao.descricao.label('TIPO'),
            Unidade.nome_instituicao.label('INSTITUICAO'),
            Unidade.cidade.label('MUNICIPIO'),
            ParecerPsicologico.descricao.label('PARECER'),
            Status.descricao.label('STATUS')
        ).outerjoin(ModalidadeEnsino, ModalidadeEnsino.id == Ator.modalidade_ensino_id)\
        .outerjoin(Profissao, Profissao.id == Ator.profissao_id)\
        .outerjoin(Unidade, Unidade.id == Ator.unidade_id)\
        .outerjoin(QuadroPsicopedagogico, QuadroPsicopedagogico.ator_id == Ator.id)\
        .outerjoin(ParecerPsicologico, ParecerPsicologico.id == QuadroPsicopedagogico.parecer_psicologico_id)\
        .outerjoin(Status, Status.codigo == Ator.status)\
        .filter(and_(*query_filters)).order_by(Ator.nome)

        if city_filter:
            ator_query = ator_query.filter(Unidade.cidade == city_filter)

        return ator_query.all()

    def get_filtered_actors_for_grid(self, query_filters, city_filter):
        ator_query = db.session.query(
            Ator.id,
            Ator.hexadecimal_foto,
            Ator.nome,
            func.timestampdiff(func.year, Ator.data_nascimento, func.now()).label('idade'),
            Ator.ano_sessao,
            ModalidadeEnsino.descricao.label('modalidade'),
            Profissao.descricao.label('tipo'),
            Unidade.nome_instituicao.label('instituicao'),
            Unidade.cidade.label('municipio'),
            ParecerPsicologico.descricao.label('parecer'),
            Status.descricao.label('status')
        ).outerjoin(ModalidadeEnsino, Ator.modalidade_ensino_id == ModalidadeEnsino.id)\
        .outerjoin(Profissao, Ator.profissao_id == Profissao.id)\
        .outerjoin(Unidade, Ator.unidade_id == Unidade.id)\
        .outerjoin(QuadroPsicopedagogico, QuadroPsicopedagogico.ator_id == Ator.id)\
        .outerjoin(ParecerPsicologico, QuadroPsicopedagogico.parecer_psicologico_id == ParecerPsicologico.id)\
        .outerjoin(Status, Ator.status == Status.codigo)\
        .filter(and_(*query_filters)).order_by(Ator.nome)

        if city_filter:
            ator_query = ator_query.filter(Unidade.cidade == city_filter)

        return ator_query.all()

    def get_all_actors_for_grid(self):
        return db.session.query(
            Ator.id,
            Ator.nome,
            Ator.email,
            Ator.ano_sessao,
            ModalidadeEnsino.descricao.label('modalidade'),
            Profissao.descricao.label('tipo'),
            Unidade.nome_instituicao.label('instituicao')
        ).outerjoin(ModalidadeEnsino, Ator.modalidade_ensino_id == ModalidadeEnsino.id)\
        .outerjoin(Profissao, Ator.profissao_id == Profissao.id)\
        .outerjoin(Unidade, Ator.unidade_id == Unidade.id)\
        .filter(Ator.status != 2).order_by(Ator.nome).all()

    def get_chat_actors_by_institution(self, unidade_id):
        atores_unidade_query = db.session.query(Ator.id, Ator.nome).filter(
            Ator.unidade_id == unidade_id,
            Ator.status != 2,
            Ator.profissao_id.in_([28, 3])
        )

        atores_profissao_query = db.session.query(Ator.id, Ator.nome).filter(
            Ator.status != 2,
            Ator.profissao_id == 100
        )

        return atores_unidade_query.union(atores_profissao_query).order_by(Ator.nome).all()

    def get_ator_name(self, ator_id):
        return Ator.query.with_entities(Ator.nome).filter_by(id=ator_id).first()

    def get_ator_messaging_data(self, ator_id):
        return db.session.query(
            Ator.id,
            Ator.nome,
            Ator.data_nascimento,
            Ator.telefone_cel,
            Ator.email,
            func.timestampdiff(func.year, Ator.data_nascimento, func.now()).label('IDADE'),
            Ator.hexadecimal_foto,
            Unidade.nome_instituicao.label('ESCOLA')
        ).outerjoin(Unidade, Unidade.id == Ator.unidade_id)\
        .filter(Ator.id == ator_id).first()

    def get_complete_ator_data(self, ator_id):
        AtorResponsavel = aliased(Ator)
        AtorInteracional = aliased(Ator)
        AtorProfessor = aliased(Ator)
        AtorPsicologo = aliased(Ator)
        
        return db.session.query(
            Ator.id,
            Ator.nome,
            Ator.data_nascimento,
            Ator.telefone_cel,
            func.timestampdiff(func.year, Ator.data_nascimento, func.now()).label('IDADE'),
            Ator.hexadecimal_foto,
            func.concat(AtorResponsavel.nome, ' ', TipoVinculo.descricao).label('RESPONSAVEL'),
            PlanoTrabalho.data_inicial_interacao.label('DATAINICIO'),
            AtorInteracional.nome.label('PARINTERACIONAL'),
            AtorProfessor.nome.label('PROFESSOR'),
            AtorPsicologo.nome.label('PSICOLOGO'),
            Unidade.nome_instituicao.label('ESCOLA'),
            Unidade.cidade.label('CIDADE'),
            Unidade.logoinstituicao.label('LOGOESCOLA'),
            AtorVinculo.ator_id.label('RESPONSAVELID'),
            PlanoTrabalho.ator_interacional_id.label('PARINTERACIONALID'),
            PlanoTrabalho.ator_professor_id.label('PROFESSORID'),
            PlanoTrabalho.ator_psicologo_id.label('PSICOLOGOID')
        ).join(AtorVinculo, AtorVinculo.ator_di_id == Ator.id)\
        .join(TipoVinculo, TipoVinculo.id == AtorVinculo.tipo_vinculo_id)\
        .join(PlanoTrabalho, PlanoTrabalho.ator_di_id == Ator.id)\
        .outerjoin(AtorResponsavel, AtorResponsavel.id == AtorVinculo.ator_id)\
        .outerjoin(AtorInteracional, AtorInteracional.id == PlanoTrabalho.ator_interacional_id)\
        .outerjoin(AtorProfessor, AtorProfessor.id == PlanoTrabalho.ator_professor_id)\
        .outerjoin(AtorPsicologo, AtorPsicologo.id == PlanoTrabalho.ator_psicologo_id)\
        .outerjoin(Unidade, Unidade.id == Ator.unidade_id)\
        .filter(Ator.id == ator_id).first()

    def get_ator_photo_hex(self, ator_id):
        return Ator.query.with_entities(Ator.hexadecimal_foto).filter_by(id=ator_id).first()

    def get_ator_by_email_for_data(self, email):
        ator = Ator.query.filter_by(email=email).first()
        if not ator:
            return None
        return {'id': ator.id, 'nome': ator.nome, 'email': ator.email}

    def get_ator_name_and_image(self, ator_id):
        return Ator.query.with_entities(Ator.nome, Ator.hexadecimal_foto).filter_by(id=ator_id).first()

    def get_ator_raw_email(self, ator_id):
        return Ator.query.with_entities(Ator.email).filter_by(id=ator_id).first()

    def check_ator_authorization(self, ator_id):
        return db.session.query(Ator.nome)\
            .join(Usuario, Usuario.email == Ator.email)\
            .filter(Ator.id == ator_id, Usuario.cod_grupo_usuario.in_([1, 3, 10, 13]))\
            .first()

    def get_all_actors_by_unidade(self, unidade_id):
        if unidade_id == 0:
            return []
        return Ator.query.with_entities(Ator.id, Ator.nome)\
            .filter(Ator.unidade_id == unidade_id, Ator.status != 2)\
            .order_by(Ator.nome).all()

    def get_students_by_unidade(self, unidade_id):
        return Ator.query.with_entities(Ator.id, Ator.nome)\
            .filter(Ator.unidade_id == unidade_id, Ator.status != 2, Ator.profissao_id == 1)\
            .order_by(Ator.nome).all()

    def get_ator_search_data(self, ator_id):
        AtorResponsavel = aliased(Ator)
        AtorInteracional = aliased(Ator)
        AtorProfessor = aliased(Ator)
        AtorPsicologo = aliased(Ator)

        return db.session.query(
            Ator.id, Ator.nome, Ator.data_nascimento, Ator.hexadecimal_foto,
            Ator.data_inicio_intervencao, Ator.ano_sessao,
            func.concat(AtorResponsavel.nome, ' ', TipoVinculo.descricao).label('RESPONSAVEL'),
            PlanoTrabalho.data_inicial_interacao.label('DATAINICIO'),
            (func.timestampdiff(func.year, Ator.data_nascimento, func.now())).label('IDADE'),
            AtorInteracional.nome.label('PARINTERACIONAL'),
            AtorProfessor.nome.label('PROFESSOR'),
            AtorPsicologo.nome.label('PSICOLOGO'),
            AtorPsicologo.email.label('EMAILPSICOLOGO'),
            AtorPsicologo.id.label('CODIGOPSICOLOGO'),
            Unidade.nome_instituicao.label('INSTITUICAO'),
            func.concat(Unidade.cidade, '-', Unidade.estado).label('MUNICIPIO'),
            AtorVinculo.ator_id.label('RESPONSAVELID'),
            PlanoTrabalho.ator_interacional_id.label('PARINTERACIONALID'),
            PlanoTrabalho.ator_professor_id.label('PROFESSORID'),
            PlanoTrabalho.ator_psicologo_id.label('PSICOLOGOID')
        ).join(AtorVinculo, AtorVinculo.ator_di_id == Ator.id)\
        .join(TipoVinculo, TipoVinculo.id == AtorVinculo.tipo_vinculo_id)\
        .join(PlanoTrabalho, PlanoTrabalho.ator_di_id == Ator.id)\
        .outerjoin(AtorResponsavel, AtorResponsavel.id == AtorVinculo.ator_id)\
        .outerjoin(AtorInteracional, AtorInteracional.id == PlanoTrabalho.ator_interacional_id)\
        .outerjoin(AtorProfessor, AtorProfessor.id == PlanoTrabalho.ator_professor_id)\
        .outerjoin(AtorPsicologo, AtorPsicologo.id == PlanoTrabalho.ator_psicologo_id)\
        .outerjoin(Unidade, Unidade.id == Ator.unidade_id)\
        .filter(Ator.id == ator_id).first()

    def get_ator_search_data_app(self, ator_id):
        subquery_so = db.session.query(
            SessaoObservacao.ator_id,
            SessaoObservacao.descricao,
            SessaoObservacao.titulo_sessao,
            func.min(SessaoObservacao.id).label('min_id')
        ).filter(
            SessaoObservacao.status == 'Criado'
        ).group_by(SessaoObservacao.ator_id).subquery('so2')

        return db.session.query(
            Ator.nome.label('RESPONSAVEL'),
            Ator.id.label('ID'),
            Ator.hexadecimal_foto.label('FOTO'),
            Ator.email.label('EMAIL'),
            Profissao.descricao.label('PROFISSAO'),
            Ator.profissao_id.label('TIPO'),
            TipoVinculo.descricao.label('VINCULO'),
            AtorVinculo.ator_di_id.label('ALUNOID'),
            subquery_so.c.descricao.label('SESSAO'),
            subquery_so.c.titulo_sessao.label('TITULO'),
            aliased(Ator, name='a2').nome.label('ALUNO')
        ).outerjoin(Profissao, Profissao.id == Ator.profissao_id)\
        .outerjoin(AtorVinculo, AtorVinculo.ator_id == Ator.id)\
        .outerjoin(TipoVinculo, TipoVinculo.id == AtorVinculo.tipo_vinculo_id)\
        .outerjoin(subquery_so, subquery_so.c.ator_id == AtorVinculo.ator_di_id)\
        .outerjoin(aliased(Ator, name='a2'), aliased(Ator, name='a2').id == AtorVinculo.ator_di_id)\
        .filter(Ator.id == ator_id).first()

    def get_student_by_responsible(self, ator_id):
        return db.session.query(
            Ator.nome.label('RESPONSAVEL'),
            Ator.id.label('ID'),
            Ator.email,
            Ator.telefone_cel,
            AtorVinculo.ator_di_id.label('ALUNOID')
        ).outerjoin(AtorVinculo, AtorVinculo.ator_id == Ator.id)\
        .filter(Ator.id == ator_id).first()

    def get_all_students_di(self):
        return Ator.query.filter(Ator.profissao_id == 1, Ator.status != 2)\
            .order_by(Ator.nome).all()

    def get_interacional_actors(self):
        atores_profissao_2_query = db.session.query(Ator.id, Ator.nome).filter(
            Ator.status != 2,
            Ator.profissao_id == 2
        )

        atores_vinculo_di_query = db.session.query(Ator.id, Ator.nome).join(
            AtorVinculo, Ator.id == AtorVinculo.ator_id
        )

        return atores_profissao_2_query.union(atores_vinculo_di_query).order_by(Ator.nome).all()

    def get_psychologists_by_city(self, city):
        unidade_ids_subquery = db.session.query(Unidade.id).filter(Unidade.cidade == city).subquery()

        ator_di_ids_subquery = db.session.query(Ator.id).filter(
            Ator.status != 2,
            Ator.profissao_id == 1,
            Ator.unidade_id.in_(unidade_ids_subquery)
        ).subquery()

        psicologo_ids_subquery = db.session.query(PlanoTrabalho.ator_psicologo_id).filter(
            PlanoTrabalho.ator_di_id.in_(ator_di_ids_subquery)
        ).group_by(PlanoTrabalho.ator_psicologo_id).subquery()

        return db.session.query(Ator.id, Ator.nome).filter(
            Ator.id.in_(psicologo_ids_subquery)
        ).order_by(Ator.nome).all()

    def get_all_psychologists(self):
        return Ator.query.filter(Ator.profissao_id == 3, Ator.status != 2)\
            .order_by(Ator.nome).all()

    def get_all_professors(self):
        return Ator.query.filter(Ator.profissao_id == 4, Ator.status != 2)\
            .order_by(Ator.nome).all()

    def get_all_responsibles(self):
        return Ator.query.filter(
            Ator.profissao_id.notin_([1, 2, 3, 4]),
            Ator.status != 2
        ).order_by(Ator.nome).all()

    def get_user_module_items_by_ator_id(self, ator_id):
        return db.session.query(
            Ator.id, Ator.nome, Ator.cpf, Ator.ano_sessao, Ator.data_nascimento,
            Ator.data_inicio_intervencao, Ator.reg_profissional, Ator.email,
            Ator.telefone_cel, Ator.telefone_fixo, Ator.idioma_id, Ator.unidade_id,
            Ator.profissao_id, Ator.endereco, Ator.cidade, Ator.estado, Ator.pais,
            Ator.hexadecimal_foto, Ator.modalidade_ensino_id, Ator.status,
            Usuario.usuario, Usuario.senha, Usuario.cod_grupo_usuario
        ).join(Usuario, Usuario.email == Ator.email)\
        .filter(Ator.id == ator_id).first()

    def get_first_ator(self):
        return Ator.query.first()