from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

from app.services.ator_service import AtorService
from app.services.auth_service import verify_token
from app.dtos.ator_dto import (
    AtorBaseDTO, AtorCreateDTO, AtorResponseDTO, AtorIdNomeDTO, AtorTipoDTO, AtorAnoSessaoDTO,
    AtorDadosMensageriaDTO, AtorDadosCompletosDTO, AtorFotoDTO, AtorByEmailDTO, AtorNomeImagemDTO,
    AtorNomeRsDTO, AtorEmailRawDTO, AtorAutorizadoDTO, AtorUnidadeDTO, AtorDadosPesquisaDTO,
    AtorDadosPesquisaAppDTO, AtorAlunoPorResponsavelDTO, AtorFilteredGridItemDTO, AtorGridItemDTO
)
from werkzeug.exceptions import HTTPException, BadRequest, Conflict, NotFound, InternalServerError


ator_ns = Namespace('Ator', description='Operações relacionadas a Atores')

ator_service = AtorService()

ator_model = ator_ns.model('Ator', {
    'id': fields.Integer(readOnly=True, description='Identificador único do ator'), 
    'nome': fields.String(required=True, description='Nome completo do ator'),
    'cpf': fields.String(description='CPF do ator'),
    'ano_sessao': fields.String(description='Ano da sessão'),
    'data_nascimento': fields.Date(description='Data de nascimento (YYYY-MM-DD)'),
    'data_inicio_intervencao': fields.Date(description='Data de início da intervenção (YYYY-MM-DD)'),
    'reg_profissional': fields.String(description='Registro profissional'),
    'email': fields.String(required=True, description='Endereço de e-mail (deve ser único)'),
    'telefone_cel': fields.String(description='Telefone celular'),
    'telefone_fixo': fields.String(description='Telefone fixo'),
    'idioma_id': fields.Integer(description='ID do idioma'),
    'unidade_id': fields.Integer(description='ID da unidade'),
    'profissao_id': fields.Integer(description='ID da profissão'),
    'endereco': fields.String(description='Endereço'),
    'cidade': fields.String(description='Cidade'),
    'estado': fields.String(description='Estado'),
    'pais': fields.String(description='País'),
    'hexadecimal_foto': fields.String(description='Nome do arquivo de foto (hexadecimal)'),
    'modalidade_ensino_id': fields.Integer(description='ID da modalidade de ensino'),
    'status': fields.Integer(description='Status do ator (ex: 1 para ativo, 2 para inativo)')
})

vinculo_data_model = ator_ns.model('VinculoData', {
    'NOMER': fields.String(required=True, description='Nome do responsável'),
    'EMAILR': fields.String(required=True, description='Email do responsável'),
    'TELEFONECEL': fields.String(description='Telefone do responsável'),
    'TIPO_VINCULO': fields.Integer(required=True, description='ID do tipo de vínculo'),
    'UNIDADEID': fields.Integer(description='ID da unidade do responsável'),
    'LOGINR': fields.String(description='Login do responsável'),
    'SENHAR': fields.String(description='Senha do responsável')
})

create_ator_request_model = ator_ns.inherit('CreateAtorRequest', ator_model, {
    'usuario': fields.String(required=True, description='Nome de usuário para login'),
    'senha': fields.String(required=True, description='Senha para login'),
    'grupo_usuario': fields.Integer(required=True, description='ID do grupo de usuário'),
    'TIPO_VINCULO': fields.Integer(description='ID do tipo de vínculo, se houver responsável'),
    'NOMER': fields.String(description='Nome do responsável (se houver vínculo)'),
    'EMAILR': fields.String(description='Email do responsável (se houver vínculo)'),
    'TELEFONECEL': fields.String(description='Telefone do responsável (se houver vínculo)'),
    'LOGINR': fields.String(description='Login do responsável (se houver vínculo)'),
    'SENHAR': fields.String(description='Senha do responsável (se houver vínculo)')
})

ator_id_nome_model = ator_ns.model('AtorIdNome', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator')
})

ator_tipo_model = ator_ns.model('AtorTipo', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'tipo': fields.String(description='Tipo (descrição da profissão) do Ator')
})

ator_ano_sessao_model = ator_ns.model('AtorAnoSessao', {
    'ano_sessao': fields.String(description='Ano da sessão do Ator')
})

ator_dados_mensageria_model = ator_ns.model('AtorDadosMensageria', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'data_nascimento': fields.Date(description='Data de nascimento (YYYY-MM-DD)'),
    'telefone_cel': fields.String(description='Telefone celular'),
    'email': fields.String(description='Endereço de e-mail'),
    'idade': fields.Integer(description='Idade do Ator'),
    'hexadecimal_foto': fields.String(description='Nome do arquivo de foto (hexadecimal)'),
    'escola': fields.String(description='Nome da Escola/Instituição')
})

ator_dados_completos_model = ator_ns.model('AtorDadosCompletos', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'data_nascimento': fields.Date(description='Data de nascimento (YYYY-MM-DD)'),
    'telefone_cel': fields.String(description='Telefone celular'),
    'idade': fields.Integer(description='Idade do Ator'),
    'hexadecimal_foto': fields.String(description='Nome do arquivo de foto (hexadecimal)'),
    'responsavel': fields.String(description='Nome e tipo de vínculo do Responsável'),
    'data_inicio': fields.Date(description='Data de início da intervenção'),
    'par_interacional': fields.String(description='Nome do Parceiro Interacional'),
    'professor': fields.String(description='Nome do Professor'),
    'psicologo': fields.String(description='Nome do Psicólogo'),
    'escola': fields.String(description='Nome da Escola/Instituição'),
    'cidade': fields.String(description='Cidade da Unidade'),
    'logo_escola': fields.String(description='Logo da Escola/Instituição'),
    'responsavel_id': fields.Integer(description='ID do Responsável'),
    'par_interacional_id': fields.Integer(description='ID do Parceiro Interacional'),
    'professor_id': fields.Integer(description='ID do Professor'),
    'psicologo_id': fields.Integer(description='ID do Psicólogo')
})

ator_foto_model = ator_ns.model('AtorFoto', {
    'hexadecimal_foto': fields.String(description='Nome do arquivo de foto (hexadecimal)')
})

ator_by_email_model = ator_ns.model('AtorByEmail', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'email': fields.String(description='Email do Ator')
})

ator_nome_imagem_model = ator_ns.model('AtorNomeImagem', {
    'nome': fields.String(description='Nome do Ator'),
    'hexadecimal_foto': fields.String(description='Nome do arquivo de foto (hexadecimal)')
})

ator_nome_rs_model = ator_ns.model('AtorNomeRs', {
    'nome': fields.String(description='Nome do Ator')
})

ator_email_raw_model = ator_ns.model('AtorEmailRaw', {
    'email': fields.String(description='Email do Ator')
})

ator_autorizado_model = ator_ns.model('AtorAutorizado', {
    'nome': fields.String(description='Nome do Ator Autorizado')
})

ator_unidade_model = ator_ns.model('AtorUnidade', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator')
})

ator_dados_pesquisa_model = ator_ns.model('AtorDadosPesquisa', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'data_nascimento': fields.Date(description='Data de nascimento (YYYY-MM-DD)'),
    'hexadecimal_foto': fields.String(description='Nome do arquivo de foto (hexadecimal)'),
    'data_inicio_intervencao': fields.Date(description='Data de início da intervenção (YYYY-MM-DD)'),
    'ano_sessao': fields.String(description='Ano da sessão'),
    'responsavel': fields.String(description='Nome e tipo de vínculo do Responsável'),
    'data_inicio': fields.Date(description='Data de início da intervenção'),
    'idade': fields.Integer(description='Idade do Ator'),
    'par_interacional': fields.String(description='Nome do Parceiro Interacional'),
    'professor': fields.String(description='Nome do Professor'),
    'psicologo': fields.String(description='Nome do Psicólogo'),
    'email_psicologo': fields.String(description='Email do Psicólogo'),
    'codigo_psicologo': fields.Integer(description='Código do Psicólogo'),
    'instituicao': fields.String(description='Nome da Instituição'),
    'municipio': fields.String(description='Município (Cidade-Estado)'),
    'responsavel_id': fields.Integer(description='ID do Responsável'),
    'par_interacional_id': fields.Integer(description='ID do Parceiro Interacional'),
    'professor_id': fields.Integer(description='ID do Professor'),
    'psicologo_id': fields.Integer(description='ID do Psicólogo')
})

ator_dados_pesquisa_app_model = ator_ns.model('AtorDadosPesquisaApp', {
    'responsavel': fields.String(description='Nome do Responsável'),
    'id': fields.Integer(description='ID do Ator'),
    'foto': fields.String(description='Nome do arquivo de foto (hexadecimal)'),
    'email': fields.String(description='Email do Ator'),
    'profissao': fields.String(description='Descrição da Profissão'),
    'tipo': fields.Integer(description='ID da Profissão'),
    'vinculo': fields.String(description='Descrição do Vínculo'),
    'aluno_id': fields.Integer(description='ID do Aluno'),
    'sessao': fields.String(description='Descrição da Sessão de Observação'),
    'titulo': fields.String(description='Título da Sessão de Observação'),
    'aluno': fields.String(description='Nome do Aluno')
})

ator_aluno_por_responsavel_model = ator_ns.model('AtorAlunoPorResponsavel', {
    'responsavel': fields.String(description='Nome do Responsável'),
    'id': fields.Integer(description='ID do Responsável'),
    'email': fields.String(description='Email do Responsável'),
    'telefone_cel': fields.String(description='Telefone celular do Responsável'),
    'aluno_id': fields.Integer(description='ID do Aluno vinculado')
})

ator_list_item_model = ator_ns.model('AtorListItem', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'email': fields.String(description='Email do Ator'),
    'cpf': fields.String(description='CPF do Ator'),
})

ator_filtered_grid_item_model = ator_ns.model('AtorFilteredGridItem', {
    'id': fields.Integer(description='ID do Ator'),
    'nome': fields.String(description='Nome do Ator'),
    'idade': fields.Integer(description='Idade do Ator'),
    'foto': fields.String(description='HTML da imagem do Ator'),
    'dados_ator': fields.String(description='Nome e idade do Ator, e ano da sessão'),
    'modalidade': fields.String(description='Modalidade de Ensino'),
    'tipo': fields.String(description='Tipo (Profissão) do Ator'),
    'instituicao': fields.String(description='Nome da Instituição'),
    'municipio': fields.String(description='Município da Instituição'),
    'parecer': fields.String(description='Parecer Psicológico'),
    'status': fields.String(description='Status do Ator')
})

ator_grid_item_model = ator_ns.model('AtorGridItem', {
    'id': fields.Integer(description='ID do Ator'),
    'dados_ator': fields.String(description='Nome, email e ano de sessões do Ator'),
    'modalidade': fields.String(description='Modalidade de Ensino'),
    'tipo': fields.String(description='Tipo (Profissão) do Ator'),
    'instituicao': fields.String(description='Nome da Instituição')
})
@ator_ns.route('')
class AtorList(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            atores = ator_service.get_all_atores()
            return [ator.to_dict() for ator in atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.expect(create_ator_request_model, validate=True)
    @ator_ns.response(201, 'Ator criado com sucesso', ator_model)
    @ator_ns.response(400, 'Erro de validação')
    @ator_ns.response(409, 'E-mail já cadastrado')
    @ator_ns.response(500, 'Erro interno do servidor')
    def post(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'write_ator'):
            ator_ns.abort(403, "Acesso negado")

        ator_create_dto = AtorCreateDTO.from_dict(ator_ns.payload)
        try:
            new_ator_model_instance = ator_service.create_ator(ator_create_dto, request.url_root)
            return "Ator criado com sucesso!", 201
        except HTTPException as e: 
            raise e 
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')
@ator_ns.route('/<int:ator_id>')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorSingle(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_model)
    @ator_ns.response(403, 'Acesso Negado')
    @ator_ns.response(404, 'Ator não encontrado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            ator = ator_service.get_ator_by_id(ator_id)
            if not ator:
                ator_ns.abort(404, "Ator não encontrado")
            return ator.to_dict()
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.expect(ator_model, validate=True) 
    @ator_ns.response(200, 'Ator atualizado com sucesso', ator_model)
    @ator_ns.response(400, 'Erro de validação')
    @ator_ns.response(403, 'Acesso Negado')
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(500, 'Erro interno do servidor')
    def put(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'write_ator'):
            ator_ns.abort(403, "Acesso negado")

        ator_base_dto = AtorBaseDTO.from_dict(ator_ns.payload)
        try:
            updated_ator = ator_service.update_ator(ator_id, ator_base_dto)
            return updated_ator.to_dict(), 200
        except ValueError as e:
            ator_ns.abort(400, str(e))
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro ao atualizar registro: {str(e)}')

    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.response(200, 'Ator deletado com sucesso')
    @ator_ns.response(403, 'Acesso Negado')
    @ator_ns.response(404, 'Ator não encontrado')
    def delete(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'write_ator'):
            ator_ns.abort(403, "Acesso negado")

        try:
            result = ator_service.soft_delete_ator(ator_id)
            return result, 200
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(404, f'Erro ao apagar registro: {str(e)}')

@ator_ns.route('/count-alunos')
class AtorCountAlunos(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.response(200, 'Contagem de alunos retornada com sucesso', fields.Integer(description='Total de alunos'))
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            count = ator_service.count_alunos()
            return {'total': count}
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/descricao')
class AtorDescricao(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_id_nome_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            atores = ator_service.get_ator_descriptions()
            return [AtorIdNomeDTO(id=a.id, nome=a.nome).to_dict() for a in atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/combo-nome')
class AtorComboNome(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(fields.String, description='Lista de nomes de atores')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            names = ator_service.get_ator_combo_names()
            return names
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/combo')
class AtorCombo(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_id_nome_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            atores = ator_service.get_ator_combo_all()
            return [AtorIdNomeDTO(id=a.id, nome=a.nome).to_dict() for a in atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/ano-sessao')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorAnoSessao(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_ano_sessao_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            ano_sessao = ator_service.get_ator_year_session(ator_id)
            return AtorAnoSessaoDTO(ano_sessao=ano_sessao).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/tipo')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorTipo(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_tipo_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            ator_data = ator_service.get_ator_type(ator_id)
            return AtorTipoDTO(**ator_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/combo-all')
class AtorComboAll(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_id_nome_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            atores = ator_service.get_ator_combo_all()
            return [AtorIdNomeDTO(id=a.id, nome=a.nome).to_dict() for a in atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/filtro-caderno-atividades')
class AtorFiltroCadernoAtividades(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @ator_ns.param('unidade_id', 'ID da unidade para filtro', type=int)
    @ator_ns.param('modalidade_ensino_id', 'ID da modalidade de ensino para filtro', type=int)
    @ator_ns.param('profissao_id', 'ID da profissão para filtro', type=int)
    @ator_ns.param('cidade', 'Cidade para filtro')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_filtered_grid_item_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        filters = {
            'unidade_id': request.args.get('unidade_id', type=int),
            'modalidade_ensino_id': request.args.get('modalidade_ensino_id', type=int),
            'profissao_id': request.args.get('profissao_id', type=int),
            'cidade': request.args.get('cidade')
        }
        try:
            results = ator_service.get_filtered_actors_for_caderno_atividades(filters)
            return [AtorFilteredGridItemDTO(**r).to_dict() for r in results]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/grid-filtro')
class AtorGridFiltro(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @ator_ns.param('unidade_id', 'ID da unidade para filtro', type=int)
    @ator_ns.param('modalidade_ensino_id', 'ID da modalidade de ensino para filtro', type=int)
    @ator_ns.param('profissao_id', 'ID da profissão para filtro', type=int)
    @ator_ns.param('cidade', 'Cidade para filtro')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_filtered_grid_item_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        filters = {
            'unidade_id': request.args.get('unidade_id', type=int),
            'modalidade_ensino_id': request.args.get('modalidade_ensino_id', type=int),
            'profissao_id': request.args.get('profissao_id', type=int),
            'cidade': request.args.get('cidade')
        }
        try:
            results = ator_service.get_filtered_actors_for_grid(filters)
            return [AtorFilteredGridItemDTO(**r).to_dict() for r in results]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/grid')
class AtorGrid(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_grid_item_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            results = ator_service.get_all_actors_for_grid()
            return [AtorGridItemDTO(**r).to_dict() for r in results]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/chat-instituicao/<int:unidade_id>')
@ator_ns.param('unidade_id', 'O identificador único da unidade')
class AtorChatInstituicao(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_id_nome_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, unidade_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            combined_atores = ator_service.get_chat_actors_by_institution(unidade_id)
            return [AtorIdNomeDTO(id=a.id, nome=a.nome).to_dict() for a in combined_atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/nome')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorNome(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_nome_rs_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            nome = ator_service.get_ator_name(ator_id)
            return AtorNomeRsDTO(nome=nome).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/dados-mensageria')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorDadosMensageria(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_dados_mensageria_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            response_data = ator_service.get_ator_messaging_data(ator_id)
            return AtorDadosMensageriaDTO(**response_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/dados-completos')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorDadosCompletos(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_dados_completos_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            response_data = ator_service.get_complete_ator_data(ator_id)
            return AtorDadosCompletosDTO(**response_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/foto')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorFoto(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_foto_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            hex_foto = ator_service.get_ator_photo_hex(ator_id)
            return AtorFotoDTO(hexadecimal_foto=hex_foto).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/email/<string:email>')
@ator_ns.param('email', 'O endereço de e-mail do ator')
class AtorByEmail(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_by_email_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, email):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            ator_data = ator_service.get_ator_by_email(email)
            return AtorByEmailDTO(**ator_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/nome-imagem')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorNomeImagem(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_nome_imagem_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            ator_data = ator_service.get_ator_name_and_image(ator_id)
            return AtorNomeImagemDTO(**ator_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/nome-rs')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorNomeRs(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_nome_rs_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            nome = ator_service.get_ator_name(ator_id)
            return AtorNomeRsDTO(nome=nome).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/email-raw')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorEmailRaw(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_email_raw_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            email = ator_service.get_ator_raw_email(ator_id)
            return AtorEmailRawDTO(email=email).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/autorizado')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorAutorizado(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_autorizado_model)
    @ator_ns.response(404, 'Ator não autorizado ou não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            ator_nome = ator_service.check_ator_authorization(ator_id)
            return AtorAutorizadoDTO(nome=ator_nome).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/unidade/<int:unidade_id>')
@ator_ns.param('unidade_id', 'O identificador único da unidade')
class AtorAllUnidade(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_unidade_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, unidade_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            atores = ator_service.get_all_actors_by_unidade(unidade_id)
            return [AtorUnidadeDTO(id=a.id, nome=a.nome).to_dict() for a in atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/unidade/<int:unidade_id>/alunos')
@ator_ns.param('unidade_id', 'O identificador único da unidade')
class AtorUnidadeAlunos(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_unidade_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, unidade_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            atores = ator_service.get_students_by_unidade(unidade_id)
            return [AtorUnidadeDTO(id=a.id, nome=a.nome).to_dict() for a in atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/dados-pesquisa')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorDadosPesquisa(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_dados_pesquisa_model)
    @ator_ns.response(404, 'Dados do ator não encontrados')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            response_data = ator_service.get_ator_search_data(ator_id)
            return AtorDadosPesquisaDTO(**response_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/dados-pesquisa-app')
@ator_ns.param('ator_id', 'O identificador único do ator')
class AtorDadosPesquisaApp(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_dados_pesquisa_app_model)
    @ator_ns.response(404, 'Dados do ator não encontrados')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            response_data = ator_service.get_ator_search_data_app(ator_id)
            return AtorDadosPesquisaAppDTO(**response_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/aluno-por-responsavel')
@ator_ns.param('ator_id', 'O identificador único do ator responsável')
class AtorAlunoPorResponsavel(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_with(ator_aluno_por_responsavel_model)
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            response_data = ator_service.get_student_by_responsible(ator_id)
            return AtorAlunoPorResponsavelDTO(**response_data).to_dict()
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/alunos-di')
class AtorAlunosDi(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_model) 
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            alunos = ator_service.get_all_students_di()
            return [AtorResponseDTO(id=a.id, **a.to_dict()).to_dict() for a in alunos]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/interacionais')
class AtorInteracionais(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_id_nome_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            combined_atores = ator_service.get_interacional_actors()
            return [AtorIdNomeDTO(id=a.id, nome=a.nome).to_dict() for a in combined_atores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/psicologos-por-cidade')
@ator_ns.param('cidade', 'Nome da cidade para filtrar psicólogos')
class AtorPsicologosPorCidade(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_id_nome_model)
    @ator_ns.response(400, 'Parâmetro "cidade" é obrigatório')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")

        cidade = request.args.get('cidade')
        try:
            psicologos = ator_service.get_psychologists_by_city(cidade)
            return [AtorIdNomeDTO(id=p.id, nome=p.nome).to_dict() for p in psicologos]
        except ValueError as e:
            ator_ns.abort(400, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/psicologos')
class AtorPsicologos(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            psicologos = ator_service.get_all_psychologists()
            return [AtorResponseDTO(id=p.id, **p.to_dict()).to_dict() for p in psicologos]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/professores')
class AtorProfessores(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            professores = ator_service.get_all_professors()
            return [AtorResponseDTO(id=p.id, **p.to_dict()).to_dict() for p in professores]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/responsaveis')
class AtorResponsaveis(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.marshal_list_with(ator_model)
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            responsaveis = ator_service.get_all_responsibles()
            return [AtorResponseDTO(id=r.id, **r.to_dict()).to_dict() for r in responsaveis]
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/itens-modulo-usuario')
class AtorItensModuloUsuario(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.response(404, 'Dados do ator não encontrados')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")
            
        try:
            response_data = ator_service.get_user_module_items_by_ator_id(ator_id)
            return response_data
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/itens-modulo')
class AtorItensModulo(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.response(200, 'Dicionário de itens do módulo retornado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")

        try:
            itens_modulo = ator_service.get_empty_module_items()
            return itens_modulo
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/<int:ator_id>/set-itens-modulo')
class AtorSetItensModulo(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(403, 'Acesso Negado')
    def get(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'read_ator'):
            ator_ns.abort(403, "Acesso negado")

        try:
            populated_items = ator_service.populate_user_module_items(ator_id)
            return populated_items
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro interno do servidor: {str(e)}')

@ator_ns.route('/perfil/<int:ator_id>')
@ator_ns.param('ator_id', 'O identificador único do ator para o perfil')
class AtorPerfilUpdate(Resource):
    @ator_ns.doc(security='Bearer Auth')
    @jwt_required()
    @ator_ns.expect(ator_model, validate=True)
    @ator_ns.response(200, 'Perfil atualizado com sucesso', ator_model)
    @ator_ns.response(400, 'Erro de validação')
    @ator_ns.response(403, 'Acesso Negado')
    @ator_ns.response(404, 'Ator não encontrado')
    @ator_ns.response(500, 'Erro interno do servidor')
    def put(self, ator_id):
        current_user_email = get_jwt_identity()
        if not verify_token(current_user_email, 'write_ator'):
            ator_ns.abort(403, "Acesso negado")

        ator_base_dto = AtorBaseDTO.from_dict(ator_ns.payload)
        try:
            updated_ator = ator_service.update_ator_profile(ator_id, ator_base_dto)
            return updated_ator.to_dict(), 200
        except ValueError as e:
            ator_ns.abort(400, str(e))
        except LookupError as e:
            ator_ns.abort(404, str(e))
        except Exception as e:
            ator_ns.abort(500, f'Erro ao atualizar perfil: {str(e)}')