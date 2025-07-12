from app.models.ator_model import Ator
from app.models.user_model import Usuario, SegProdCognvoxUsuario
from app.models.ator_vinculo_model import AtorVinculo
from app.services.auth_service import base64_encode_py, remove_accents_py, send_email_py
from app.validators.ator_validator import validate_ator_data, validate_vinculo_data
from app.dtos.ator_dto import AtorCreateDTO, AtorBaseDTO
from app.exceptions.custom_exceptions import HttpConflictError, HttpBadRequestError, HttpInternalServerError, HttpNotFoundError
from app.repositories.ator_repository import AtorRepository 
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
import sys

class AtorService:
    def __init__(self):
        self.ator_repository = AtorRepository()

    def _build_ator_filter_query(self, filters):
        query_filters = [Ator.status != 2]
        unidade_id = filters.get('unidade_id')
        modalidade_ensino_id = filters.get('modalidade_ensino_id')
        profissao_id = filters.get('profissao_id')
        cidade = filters.get('cidade')
        if unidade_id is not None and str(unidade_id) != "0" and str(unidade_id) != "":
            query_filters.append(Ator.unidade_id == unidade_id)
        if modalidade_ensino_id is not None and str(modalidade_ensino_id) != "0" and str(modalidade_ensino_id) != "":
            query_filters.append(Ator.modalidade_ensino_id == modalidade_ensino_id)
        if profissao_id is not None and str(profissao_id) != "0" and str(profissao_id) != "":
            query_filters.append(Ator.profissao_id == profissao_id)
        if not (unidade_id or modalidade_ensino_id or profissao_id or cidade):
            query_filters.append(Ator.unidade_id == 0)
        return query_filters

    def get_all_atores(self):
        return self.ator_repository.get_all_atores()

    def get_ator_by_id(self, ator_id):
        return self.ator_repository.get_ator_by_id(ator_id)

    def create_ator(self, ator_dto: AtorCreateDTO, request_url_root: str):
        is_valid, error_message = validate_ator_data(ator_dto.to_dict())
        if not is_valid:
            raise HttpBadRequestError(error_message)

        if self.ator_repository.get_ator_by_email(ator_dto.email):
            raise HttpConflictError('Já existe esse email cadastrado em nossos registros!')

        if self.ator_repository.get_user_by_username(ator_dto.usuario):
            raise HttpConflictError('Já existe um usuário com este nome de usuário cadastrado!')

        if ator_dto.cpf and self.ator_repository.get_ator_by_cpf(ator_dto.cpf):
            raise HttpConflictError('Já existe esse CPF cadastrado em nossos registros!')

        data_inicio_intervencao = ator_dto.data_inicio_intervencao or date.today()

        try:
            with self.ator_repository.begin_nested():
                new_ator = Ator(
                    nome=ator_dto.nome,
                    cpf=ator_dto.cpf,
                    data_nascimento=ator_dto.data_nascimento,
                    data_inicio_intervencao=data_inicio_intervencao,
                    reg_profissional=ator_dto.reg_profissional,
                    email=ator_dto.email,
                    telefone_cel=ator_dto.telefone_cel,
                    telefone_fixo=ator_dto.telefone_fixo,
                    idioma_id=ator_dto.idioma_id,
                    unidade_id=ator_dto.unidade_id,
                    profissao_id=ator_dto.profissao_id,
                    endereco=ator_dto.endereco,
                    cidade=ator_dto.cidade,
                    estado=ator_dto.estado,
                    pais=ator_dto.pais,
                    hexadecimal_foto=ator_dto.hexadecimal_foto or '',
                    modalidade_ensino_id=ator_dto.modalidade_ensino_id,
                    status=ator_dto.status,
                    ano_sessao=ator_dto.ano_sessao
                )
                self.ator_repository.add_ator(new_ator)
                self.ator_repository.flush()

                new_user = Usuario(
                    usuario=ator_dto.usuario,
                    senha=base64_encode_py(ator_dto.senha),
                    cod_empresa=ator_dto.unidade_id,
                    nome=ator_dto.nome,
                    email=ator_dto.email,
                    cod_status=1,
                    cod_grupo_usuario=ator_dto.grupo_usuario,
                    cod_nivel=1,
                    primeiro_acesso=1,
                    erros_login=0
                )
                self.ator_repository.add_user(new_user)
                self.ator_repository.flush()

                new_sec_user = SegProdCognvoxUsuario(
                    usuario=base64_encode_py(ator_dto.usuario),
                    senha=base64_encode_py(ator_dto.senha),
                    cod_status=1,
                    cod_ordenacao=new_user.codigo
                )
                self.ator_repository.add_sec_user(new_sec_user)
                
                if ator_dto.tipo_vinculo:
                    vinculo_data_for_validation = {
                        'NOMER': ator_dto.nome_responsavel,
                        'EMAILR': ator_dto.email_responsavel,
                        'TELEFONECEL': ator_dto.telefone_cel_responsavel,
                        'TIPO_VINCULO': ator_dto.tipo_vinculo,
                        'UNIDADEID': ator_dto.unidade_id,
                        'LOGINR': ator_dto.login_responsavel,
                        'SENHAR': ator_dto.senha_responsavel
                    }
                    is_valid_vinculo, vinculo_error = validate_vinculo_data(vinculo_data_for_validation)
                    if not is_valid_vinculo:
                        raise HttpBadRequestError(f"Erro nos dados do vínculo: {vinculo_error}")

                    new_responsible_ator = Ator(
                        nome=ator_dto.nome_responsavel,
                        data_inicio_intervencao=data_inicio_intervencao,
                        data_nascimento=date.today(),
                        email=ator_dto.email_responsavel,
                        telefone_cel=ator_dto.telefone_cel_responsavel,
                        idioma_id=ator_dto.idioma_id,
                        unidade_id=ator_dto.unidade_id,
                        profissao_id=28,
                        endereco=ator_dto.endereco,
                        cidade=ator_dto.cidade,
                        estado=ator_dto.estado,
                        pais=ator_dto.pais,
                        modalidade_ensino_id=ator_dto.modalidade_ensino_id,
                        status=ator_dto.status,
                        ano_sessao=1
                    )
                    self.ator_repository.add_ator(new_responsible_ator)
                    self.ator_repository.flush()

                    new_responsible_user = Usuario(
                        usuario=ator_dto.login_responsavel,
                        senha=base64_encode_py(ator_dto.senha_responsavel),
                        cod_empresa=ator_dto.unidade_id,
                        nome=ator_dto.nome_responsavel,
                        email=ator_dto.email_responsavel,
                        cod_status=1,
                        cod_grupo_usuario=ator_dto.grupo_usuario,
                        cod_nivel=1,
                        primeiro_acesso=1,
                        erros_login=0
                    )
                    self.ator_repository.add_user(new_responsible_user)
                    self.ator_repository.flush()

                    new_responsible_sec_user = SegProdCognvoxUsuario(
                        usuario=base64_encode_py(ator_dto.login_responsavel),
                        senha=base64_encode_py(ator_dto.senha_responsavel),
                        cod_status=1,
                        cod_ordenacao=new_responsible_user.codigo
                    )
                    self.ator_repository.add_sec_user(new_responsible_sec_user)
                    
                    new_ator_vinculo = AtorVinculo(
                        ator_id=new_responsible_ator.id,
                        ator_di_id=new_ator.id,
                        tipo_vinculo_id=ator_dto.tipo_vinculo
                    )
                    self.ator_repository.add_ator_vinculo(new_ator_vinculo)

            self.ator_repository.commit()

            if ator_dto.status != 2:
                subject = "DADOS DE ACESSO AO COGNVOX"
                body = f"""
                <div style="text-align: center;"><img src="{request_url_root.rstrip('/')}/images/logoOficial.png" height=50></div>
                <p>Seus dados foram alterados em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.</p>
                <h3>Usuário: {remove_accents_py(ator_dto.usuario)}</h3><br>
                <h3>Senha: {remove_accents_py(ator_dto.senha)}</h3><br>
                <h3>E-Mail: {remove_accents_py(ator_dto.email)}</h3><br>
                <p>No próximo login no COGNVOX, utilize o LOGIN e SENHA informados aqui para ter acesso.</p>
                <div style="text-align: center;" ><a href="{request_url_root.rstrip('/')}">ACESSE AQUI</a></div><br>
                <div style="text-align: center;"><hr><p><b>Caso deseje remover seus dados da plataforma clique em <a href="{request_url_root.rstrip('/')}/excluiusuario/">REMOVER MEUS DADOS DA PLATAFORMA</a>.</b></p></div>
                <div style="text-align: center;"><hr><p><b>Este é um email automático, não deve ser respondido.</b></p></div>
                """
                send_email_py(ator_dto.email, None, "suporte@cognivox.net", subject, body)
            
            return new_ator

        except IntegrityError as e:
            self.ator_repository.rollback()
            if "Duplicate entry" in str(e):
                raise HttpConflictError(f"Erro de duplicidade no banco de dados: {str(e)}") from e
            elif "foreign key constraint fails" in str(e):
                raise HttpBadRequestError(f"Erro de chave estrangeira: {str(e)}") from e
            else:
                raise HttpInternalServerError(f"Erro inesperado no banco de dados: {str(e)}") from e
        except Exception as e:
            self.ator_repository.rollback()
            raise

    def update_ator(self, ator_id: int, ator_dto: AtorBaseDTO):
        is_valid, error_message = validate_ator_data(ator_dto.to_dict(), is_update=True)
        if not is_valid:
            raise ValueError(error_message)

        ator_to_update = self.ator_repository.get_ator_by_id(ator_id)
        if not ator_to_update:
            raise LookupError("Ator não encontrado")
            
        old_email = ator_to_update.email
        
        try:
            with self.ator_repository.begin_nested():
                ator_to_update.nome = ator_dto.nome
                ator_to_update.cpf = ator_dto.cpf
                ator_to_update.data_nascimento = ator_dto.data_nascimento
                ator_to_update.data_inicio_intervencao = ator_dto.data_inicio_intervencao
                ator_to_update.reg_profissional = ator_dto.reg_profissional
                ator_to_update.email = ator_dto.email
                ator_to_update.telefone_cel = ator_dto.telefone_cel
                ator_to_update.telefone_fixo = ator_dto.telefone_fixo
                ator_to_update.idioma_id = ator_dto.idioma_id
                ator_to_update.unidade_id = ator_dto.unidade_id
                ator_to_update.profissao_id = ator_dto.profissao_id
                ator_to_update.endereco = ator_dto.endereco
                ator_to_update.cidade = ator_dto.cidade
                ator_to_update.estado = ator_dto.estado
                ator_to_update.pais = ator_dto.pais
                ator_to_update.hexadecimal_foto = ator_dto.hexadecimal_foto
                ator_to_update.modalidade_ensino_id = ator_dto.modalidade_ensino_id
                ator_to_update.status = ator_dto.status
                ator_to_update.ano_sessao = ator_dto.ano_sessao
                
                self.ator_repository.update_plano_trabalho_by_ator_id(ator_id, {'data_inicial_interacao': ator_dto.data_inicio_intervencao})

                user_to_update = self.ator_repository.get_user_by_email(old_email)
                if user_to_update:
                    user_to_update.usuario = ator_dto.usuario
                    user_to_update.nome = ator_dto.nome
                    if ator_dto.senha:
                        user_to_update.senha = base64_encode_py(ator_dto.senha)
                    user_to_update.email = ator_dto.email
                    user_to_update.cod_empresa = ator_dto.unidade_id
                    user_to_update.cpf = ator_dto.cpf
                    user_to_update.cod_status = ator_dto.status

                user_main = self.ator_repository.get_user_by_email(ator_dto.email)
                if user_main:
                    sec_user_to_update = self.ator_repository.get_sec_user_by_cod_ordenacao(user_main.codigo)
                    if sec_user_to_update:
                        sec_user_to_update.usuario = base64_encode_py(ator_dto.usuario)
                        if ator_dto.senha:
                            sec_user_to_update.senha = base64_encode_py(ator_dto.senha)
                        sec_user_to_update.cod_status = ator_dto.status
            
            self.ator_repository.commit()
            
            return ator_to_update

        except Exception as e:
            self.ator_repository.rollback()
            print(f"Erro ao atualizar perfil: {e}", sys.exc_info())
            raise

    def soft_delete_ator(self, ator_id):
        ator_to_delete = self.ator_repository.get_ator_by_id(ator_id)
        if not ator_to_delete:
            raise HttpNotFoundError("Ator não encontrado")
        
        try:
            ator_to_delete.status = 2
            self.ator_repository.commit()
            return {'message': 'Registro apagado com sucesso!'}
        except Exception as e:
            self.ator_repository.rollback()
            print(f"Erro ao apagar ator: {e}", sys.exc_info())
            raise

    def count_alunos(self):
        return self.ator_repository.count_alunos()

    def get_ator_descriptions(self):
        return self.ator_repository.get_ator_descriptions()

    def get_ator_combo_names(self):
        return self.ator_repository.get_ator_combo_names()

    def get_ator_combo_all(self):
        return self.ator_repository.get_ator_combo_all()

    def get_ator_year_session(self, ator_id):
        ator = self.ator_repository.get_ator_year_session(ator_id)
        if not ator:
            raise LookupError('Ator não encontrado')
        return ator.ano_sessao

    def get_ator_type(self, ator_id):
        ator_data = self.ator_repository.get_ator_type(ator_id)

        if not ator_data:
            raise LookupError('Ator não encontrado')
        
        return {
            'id': ator_data.id,
            'nome': ator_data.nome,
            'tipo': ator_data.tipo
        }

    def get_filtered_actors_for_caderno_atividades(self, filters):
        query_filters = self._build_ator_filter_query(filters)
        city_filter = filters.get('cidade') if str(filters.get('cidade')) not in ["0", ""] else None
        
        atores = self.ator_repository.get_filtered_actors_for_caderno_atividades(query_filters, city_filter)
        
        results = []
        for ator in atores:
            foto_html = f'<img class="image-2" src="/md_arquivos/upload/deposito/{ator.hexadecimal_foto}">' if ator.hexadecimal_foto and len(ator.hexadecimal_foto) > 3 else '<img class="image-2" src="/images/aluno_default.png">'
            
            dados_ator = f"{ator.nome}<br>{ator.IDADE} anos"
            if ator.ano_sessao not in [None, ""]:
                dados_ator += f"<br>SESSÃO ANO:{ator.ano_sessao}"
                
            results.append({
                'id': ator.id,
                'nome': ator.nome,
                'idade': ator.IDADE,
                'foto': foto_html,
                'dados_ator': dados_ator,
                'modalidade': ator.MODALIDADE,
                'tipo': ator.TIPO,
                'instituicao': ator.INSTITUICAO,
                'municipio': ator.MUNICIPIO,
                'parecer': ator.PARECER,
                'status': ator.STATUS
            })
        return results

    def get_filtered_actors_for_grid(self, filters):
        query_filters = self._build_ator_filter_query(filters)
        city_filter = filters.get('cidade') if str(filters.get('cidade')) not in ["0", ""] else None

        atores = self.ator_repository.get_filtered_actors_for_grid(query_filters, city_filter)
        
        results = []
        for ator in atores:
            foto_html = f'<div class="col-md-12 justify-content-center"><img class="image-2 col-md-10" src="/md_arquivos/upload/deposito/{ator.hexadecimal_foto}"></div>' if ator.hexadecimal_foto else '<div class="col-md-12 justify-content-center"><img class="image-2 col-md-10" src="/images/aluno_default.png"></div>'
            
            dados_ator = f"{ator.nome}<br>{ator.idade} anos"
            if ator.ano_sessao not in [None, ""]:
                dados_ator += f"<br>SESSÃO ANO:{ator.ano_sessao}"
                
            results.append({
                'id': ator.id,
                'foto': foto_html,
                'dados_ator': dados_ator,
                'modalidade': ator.modalidade,
                'tipo': ator.tipo,
                'instituicao': ator.instituicao,
                'municipio': ator.municipio,
                'parecer': ator.parecer,
                'status': ator.status
            })
        return results

    def get_all_actors_for_grid(self):
        atores = self.ator_repository.get_all_actors_for_grid()

        results = []
        for ator in atores:
            dados_ator = f"{ator.nome}<br>{ator.email}"
            if ator.ano_sessao:
                dados_ator += f"<br>Sessões ano:{ator.ano_sessao}"
                
            results.append({
                'id': ator.id,
                'dados_ator': dados_ator,
                'modalidade': ator.modalidade,
                'tipo': ator.tipo,
                'instituicao': ator.instituicao
            })
        return results

    def get_chat_actors_by_institution(self, unidade_id):
        combined_atores = self.ator_repository.get_chat_actors_by_institution(unidade_id)
        
        return [{'id': a.id, 'nome': a.nome} for a in combined_atores]

    def get_ator_name(self, ator_id):
        ator = self.ator_repository.get_ator_name(ator_id)
        if not ator:
            raise LookupError('Ator não encontrado')
        return ator.nome

    def get_ator_messaging_data(self, ator_id):
        ator_data = self.ator_repository.get_ator_messaging_data(ator_id)

        if not ator_data:
            raise LookupError('Ator não encontrado')
            
        return {
            'id': ator_data.id,
            'nome': ator_data.nome,
            'data_nascimento': ator_data.data_nascimento.isoformat() if ator_data.data_nascimento else None,
            'telefone_cel': ator_data.telefone_cel,
            'email': ator_data.email,
            'idade': ator_data.IDADE,
            'hexadecimal_foto': ator_data.hexadecimal_foto,
            'escola': ator_data.ESCOLA
        }

    def get_complete_ator_data(self, ator_id):
        result = self.ator_repository.get_complete_ator_data(ator_id)
        
        if not result:
            raise LookupError('Ator não encontrado')
            
        return {
            'id': result.id,
            'nome': result.nome,
            'data_nascimento': result.data_nascimento.isoformat() if result.data_nascimento else None,
            'telefone_cel': result.telefone_cel,
            'idade': result.IDADE,
            'hexadecimal_foto': result.hexadecimal_foto,
            'responsavel': result.RESPONSAVEL,
            'data_inicio': result.DATAINICIO.isoformat() if result.DATAINICIO else None,
            'par_interacional': result.PARINTERACIONAL,
            'professor': result.PROFESSOR,
            'psicologo': result.PSICOLOGO,
            'escola': result.ESCOLA,
            'cidade': result.CIDADE,
            'logo_escola': result.LOGOESCOLA,
            'responsavel_id': result.RESPONSAVELID,
            'par_interacional_id': result.PARINTERACIONALID,
            'professor_id': result.PROFESSORID,
            'psicologo_id': result.PSICOLOGOID
        }

    def get_ator_photo_hex(self, ator_id):
        ator = self.ator_repository.get_ator_photo_hex(ator_id)
        if not ator:
            raise LookupError('Ator não encontrado')
        return ator.hexadecimal_foto

    def get_ator_by_email(self, email):
        ator = self.ator_repository.get_ator_by_email_for_data(email)
        if not ator:
            raise LookupError('Ator não encontrado')
        return ator

    def get_ator_name_and_image(self, ator_id):
        ator = self.ator_repository.get_ator_name_and_image(ator_id)
        if not ator:
            raise LookupError('Ator não encontrado')
        return {'nome': ator.nome, 'hexadecimal_foto': ator.hexadecimal_foto}

    def get_ator_raw_email(self, ator_id):
        ator = self.ator_repository.get_ator_raw_email(ator_id)
        if not ator:
            raise LookupError('Ator não encontrado')
        return ator.email

    def check_ator_authorization(self, ator_id):
        ator_autorizado = self.ator_repository.check_ator_authorization(ator_id)

        if not ator_autorizado:
            raise LookupError('Ator não autorizado ou não encontrado')
        return ator_autorizado.nome

    def get_all_actors_by_unidade(self, unidade_id):
        return self.ator_repository.get_all_actors_by_unidade(unidade_id)

    def get_students_by_unidade(self, unidade_id):
        return self.ator_repository.get_students_by_unidade(unidade_id)

    def get_ator_search_data(self, ator_id):
        ator_data = self.ator_repository.get_ator_search_data(ator_id)

        if not ator_data:
            raise LookupError('Dados do ator não encontrados')

        return {
            'id': ator_data.id,
            'nome': ator_data.nome,
            'data_nascimento': ator_data.data_nascimento.isoformat() if ator_data.data_nascimento else None,
            'hexadecimal_foto': ator_data.hexadecimal_foto,
            'data_inicio_intervencao': ator_data.data_inicio_intervencao.isoformat() if ator_data.data_inicio_intervencao else None,
            'ano_sessao': ator_data.ano_sessao,
            'responsavel': ator_data.RESPONSAVEL,
            'data_inicio': ator_data.DATAINICIO.isoformat() if ator_data.DATAINICIO else None,
            'idade': ator_data.IDADE,
            'par_interacional': ator_data.PARINTERACIONAL,
            'professor': ator_data.PROFESSOR,
            'psicologo': ator_data.PSICOLOGO,
            'email_psicologo': ator_data.EMAILPSICOLOGO,
            'codigo_psicologo': ator_data.CODIGOPSICOLOGO,
            'instituicao': ator_data.INSTITUICAO,
            'municipio': ator_data.MUNICIPIO,
            'responsavel_id': ator_data.RESPONSAVELID,
            'par_interacional_id': ator_data.PARINTERACIONALID,
            'professor_id': ator_data.PROFESSORID,
            'psicologo_id': ator_data.PSICOLOGOID
        }

    def get_ator_search_data_app(self, ator_id):
        ator_data = self.ator_repository.get_ator_search_data_app(ator_id)

        if not ator_data:
            raise LookupError('Dados do ator não encontrados')

        return {
            'responsavel': ator_data.RESPONSAVEL,
            'id': ator_data.ID,
            'foto': ator_data.FOTO,
            'email': ator_data.EMAIL,
            'profissao': ator_data.PROFISSAO,
            'tipo': ator_data.TIPO,
            'vinculo': ator_data.VINCULO,
            'aluno_id': ator_data.ALUNOID,
            'sessao': ator_data.SESSAO,
            'titulo': ator_data.TITULO,
            'aluno': ator_data.ALUNO
        }

    def get_student_by_responsible(self, ator_id):
        ator_data = self.ator_repository.get_student_by_responsible(ator_id)

        if not ator_data:
            raise LookupError('Ator não encontrado')

        return {
            'responsavel': ator_data.RESPONSAVEL,
            'id': ator_data.ID,
            'email': ator_data.email,
            'telefone_cel': ator_data.telefone_cel,
            'aluno_id': ator_data.ALUNOID
        }

    def get_all_students_di(self):
        return self.ator_repository.get_all_students_di()

    def get_interacional_actors(self):
        combined_atores = self.ator_repository.get_interacional_actors()
        
        return [{'id': a.id, 'nome': a.nome} for a in combined_atores]

    def get_psychologists_by_city(self, city):
        if not city:
            raise ValueError('Parâmetro "cidade" é obrigatório')

        psicologos = self.ator_repository.get_psychologists_by_city(city)
        
        return [{'id': p.id, 'nome': p.nome} for p in psicologos]

    def get_all_psychologists(self):
        return self.ator_repository.get_all_psychologists()

    def get_all_professors(self):
        return self.ator_repository.get_all_professors()

    def get_all_responsibles(self):
        return self.ator_repository.get_all_responsibles()

    def get_user_module_items_by_ator_id(self, ator_id):
        ator_data = self.ator_repository.get_user_module_items_by_ator_id(ator_id)

        if not ator_data:
            raise LookupError('Dados do ator não encontrados')
            
        return {
            'ID': ator_data.id,
            'NOME': ator_data.nome,
            'CPF': ator_data.cpf,
            'ANO_SESSAO': ator_data.ano_sessao,
            'DATANASCIMENTO': ator_data.data_nascimento.isoformat() if ator_data.data_nascimento else None,
            'DATAINICIOINTERVENCAO': ator_data.data_inicio_intervencao.isoformat() if ator_data.data_inicio_intervencao else None,
            'REGPROFISSIONAL': ator_data.reg_profissional,
            'EMAIL': ator_data.email,
            'TELEFONECEL': ator_data.telefone_cel,
            'TELEFONEFIXO': ator_data.telefone_fixo,
            'IDIOMAID': ator_data.idioma_id,
            'UNIDADEID': ator_data.unidade_id,
            'PROFISSAOID': ator_data.profissao_id,
            'ENDERECO': ator_data.endereco,
            'CIDADE': ator_data.cidade,
            'ESTADO': ator_data.estado,
            'PAIS': ator_data.pais,
            'HEXADECIMALFOTO': ator_data.hexadecimal_foto,
            'MODALIDADEENSINOID': ator_data.modalidade_ensino_id,
            'STATUS': ator_data.status,
            'USUARIO': ator_data.usuario,
            'SENHA': ator_data.senha,
            'COD_GRUPO_USUARIO': ator_data.cod_grupo_usuario
        }

    def get_empty_module_items(self):
        first_ator = self.ator_repository.get_first_ator()
        if first_ator:
            return {key.upper(): "" for key in first_ator.__table__.columns.keys()}
        return {}

    def populate_user_module_items(self, ator_id):
        ator_data = self.ator_repository.get_user_module_items_by_ator_id(ator_id)

        if not ator_data:
            raise LookupError('Ator não encontrado')
            
        return {
            'ID': ator_data.id,
            'NOME': ator_data.nome,
            'CPF': ator_data.cpf,
            'ANO_SESSAO': ator_data.ano_sessao,
            'DATANASCIMENTO': ator_data.data_nascimento.isoformat() if ator_data.data_nascimento else None,
            'DATAINICIOINTERVENCAO': ator_data.data_inicio_intervencao.isoformat() if ator_data.data_inicio_intervencao else None,
            'REGPROFISSIONAL': ator_data.reg_profissional,
            'EMAIL': ator_data.email,
            'TELEFONECEL': ator_data.telefone_cel,
            'TELEFONECELO': ator_data.telefone_cel,
            'TELEFONEFIXO': ator_data.telefone_fixo,
            'IDIOMAID': ator_data.idioma_id,
            'UNIDADEID': ator_data.unidade_id,
            'PROFISSAOID': ator_data.profissao_id,
            'ENDERECO': ator_data.endereco,
            'CIDADE': ator_data.cidade,
            'ESTADO': ator_data.estado,
            'PAIS': ator_data.pais,
            'HEXADECIMALFOTO': ator_data.hexadecimal_foto,
            'MODALIDADEENSINOID': ator_data.modalidade_ensino_id,
            'STATUS': ator_data.status,
            'USUARIO': ator_data.usuario,
            'SENHA': ator_data.senha,
            'COD_GRUPO_USUARIO': ator_data.cod_grupo_usuario
        }

    def update_ator_profile(self, ator_id, data):
        data['id'] = ator_id
        is_valid, error_message = validate_ator_data(data, is_update=True)
        if not is_valid:
            raise ValueError(error_message)

        ator_to_update = self.ator_repository.get_ator_by_id(ator_id)
        if not ator_to_update:
            raise LookupError("Ator não encontrado")
            
        old_email = ator_to_update.email
        
        try:
            with self.ator_repository.begin_nested():
                ator_to_update.nome = data.get('nome', ator_to_update.nome)
                ator_to_update.cpf = data.get('cpf', ator_to_update.cpf)
                ator_to_update.data_nascimento = data.get('data_nascimento', ator_to_update.data_nascimento)
                ator_to_update.data_inicio_intervencao = data.get('data_inicio_intervencao', ator_to_update.data_inicio_intervencao)
                ator_to_update.reg_profissional = data.get('reg_profissional', ator_to_update.reg_profissional)
                ator_to_update.email = data.get('email', ator_to_update.email)
                ator_to_update.telefone_cel = data.get('telefone_cel', ator_to_update.telefone_cel)
                ator_to_update.telefone_fixo = data.get('telefone_fixo', ator_to_update.telefone_fixo)
                ator_to_update.idioma_id = data.get('idioma_id', ator_to_update.idioma_id)
                ator_to_update.unidade_id = data.get('unidade_id', ator_to_update.unidade_id)
                ator_to_update.profissao_id = data.get('profissao_id', ator_to_update.profissao_id)
                ator_to_update.endereco = data.get('endereco', ator_to_update.endereco)
                ator_to_update.cidade = data.get('cidade', ator_to_update.cidade)
                ator_to_update.estado = data.get('estado', ator_to_update.estado)
                ator_to_update.pais = data.get('pais', ator_to_update.pais)
                ator_to_update.hexadecimal_foto = data.get('hexadecimal_foto', ator_to_update.hexadecimal_foto)
                ator_to_update.modalidade_ensino_id = data.get('modalidade_ensino_id', ator_to_update.modalidade_ensino_id)
                ator_to_update.status = data.get('status', ator_to_update.status)
                
                user_to_update = self.ator_repository.get_user_by_email(old_email)
                if user_to_update:
                    user_to_update.usuario = data.get('usuario', user_to_update.usuario)
                    user_to_update.nome = data.get('nome', user_to_update.nome)
                    if 'senha' in data and data['senha']:
                        user_to_update.senha = base64_encode_py(data['senha'])
                    user_to_update.email = data.get('email', user_to_update.email)
                    user_to_update.cod_empresa = data.get('unidade_id', user_to_update.cod_empresa)
                    user_to_update.cpf = data.get('cpf', user_to_update.cpf)
                    user_to_update.cod_status = data.get('status', user_to_update.cod_status)

                user_main = self.ator_repository.get_user_by_email(data.get('email', old_email))
                if user_main:
                    sec_user_to_update = self.ator_repository.get_sec_user_by_cod_ordenacao(user_main.codigo)
                    if sec_user_to_update:
                        sec_user_to_update.usuario = base64_encode_py(data.get('usuario', sec_user_to_update.usuario))
                        if 'senha' in data and data['senha']:
                            sec_user_to_update.senha = base64_encode_py(data['senha'])
                        sec_user_to_update.cod_status = data.get('status', sec_user_to_update.cod_status)
            
            self.ator_repository.commit()
            
            return ator_to_update

        except Exception as e:
            self.ator_repository.rollback()
            print(f"Erro ao atualizar perfil: {e}", sys.exc_info())
            raise