from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List, Dict, Any

@dataclass
class AtorBaseDTO:
    nome: str
    email: str
    usuario: str
    senha: str
    grupo_usuario: int
    cpf: Optional[str] = None
    ano_sessao: Optional[str] = None
    data_nascimento: Optional[date] = None
    data_inicio_intervencao: Optional[date] = None
    reg_profissional: Optional[str] = None
    telefone_cel: Optional[str] = None
    telefone_fixo: Optional[str] = None
    idioma_id: Optional[int] = None
    unidade_id: Optional[int] = None
    profissao_id: Optional[int] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    hexadecimal_foto: Optional[str] = None
    modalidade_ensino_id: Optional[int] = None
    status: Optional[int] = None

    def to_dict(self):
        data_dict = {}
        for field_name in self.__dataclass_fields__.keys(): 
            value = getattr(self, field_name)
            if isinstance(value, date):
                data_dict[field_name] = value.isoformat()
            elif value is not None:
                data_dict[field_name] = value
        return data_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        processed_data = data.copy()
        for date_field in ['data_nascimento', 'data_inicio_intervencao']:
            if date_field in processed_data and isinstance(processed_data[date_field], str):
                try:
                    processed_data[date_field] = date.fromisoformat(processed_data[date_field])
                except ValueError:
                    processed_data[date_field] = None
        
        valid_keys = set(cls.__dataclass_fields__.keys()) 
        filtered_data = {k: v for k, v in processed_data.items() if k in valid_keys}
        
        return cls(**filtered_data)


@dataclass
class AtorCreateDTO(AtorBaseDTO):
    tipo_vinculo: Optional[int] = None
    nome_responsavel: Optional[str] = None
    email_responsavel: Optional[str] = None
    telefone_cel_responsavel: Optional[str] = None
    login_responsavel: Optional[str] = None
    senha_responsavel: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        processed_data = data.copy()
        for date_field in ['data_nascimento', 'data_inicio_intervencao']:
            if date_field in processed_data and isinstance(processed_data[date_field], str):
                try:
                    processed_data[date_field] = date.fromisoformat(processed_data[date_field])
                except ValueError:
                    processed_data[date_field] = None

        if 'TIPO_VINCULO' in processed_data:
            processed_data['tipo_vinculo'] = processed_data.pop('TIPO_VINCULO')
        if 'NOMER' in processed_data:
            processed_data['nome_responsavel'] = processed_data.pop('NOMER')
        if 'EMAILR' in processed_data:
            processed_data['email_responsavel'] = processed_data.pop('EMAILR')
        if 'TELEFONECEL' in processed_data:
            processed_data['telefone_cel_responsavel'] = processed_data.pop('TELEFONECEL')
        if 'LOGINR' in processed_data:
            processed_data['login_responsavel'] = processed_data.pop('LOGINR')
        if 'SENHAR' in processed_data:
            processed_data['senha_responsavel'] = processed_data.pop('SENHAR')

        valid_keys = set(cls.__dataclass_fields__.keys())
        filtered_data = {k: v for k, v in processed_data.items() if k in valid_keys}
        
        return cls(**filtered_data)


@dataclass
class AtorResponseDTO(AtorBaseDTO):
    id: Optional[int] = None


@dataclass
class AtorIdNomeDTO:
    id: int
    nome: str


@dataclass
class AtorTipoDTO:
    id: int
    nome: str
    tipo: str


@dataclass
class AtorAnoSessaoDTO:
    ano_sessao: str


@dataclass
class AtorDadosMensageriaDTO:
    id: int
    nome: str
    data_nascimento: Optional[date]
    telefone_cel: Optional[str]
    email: str
    idade: Optional[int]
    hexadecimal_foto: Optional[str]
    escola: Optional[str]

    def to_dict(self):
        data_dict = {}
        for field_name in self.__dataclass_fields__.keys():
            value = getattr(self, field_name)
            if isinstance(value, date):
                data_dict[field_name] = value.isoformat()
            elif value is not None:
                data_dict[field_name] = value
        return data_dict


@dataclass
class AtorDadosCompletosDTO:
    id: int
    nome: str
    data_nascimento: Optional[date]
    telefone_cel: Optional[str]
    idade: Optional[int]
    hexadecimal_foto: Optional[str]
    responsavel: Optional[str]
    data_inicio: Optional[date]
    par_interacional: Optional[str]
    professor: Optional[str]
    psicologo: Optional[str]
    escola: Optional[str]
    cidade: Optional[str]
    logo_escola: Optional[str]
    responsavel_id: Optional[int]
    par_interacional_id: Optional[int]
    professor_id: Optional[int]
    psicologo_id: Optional[int]

    def to_dict(self):
        data_dict = {}
        for field_name in self.__dataclass_fields__.keys():
            value = getattr(self, field_name)
            if isinstance(value, date):
                data_dict[field_name] = value.isoformat()
            elif value is not None:
                data_dict[field_name] = value
        return data_dict


@dataclass
class AtorFotoDTO:
    hexadecimal_foto: Optional[str]


@dataclass
class AtorByEmailDTO:
    id: int
    nome: str
    email: str


@dataclass
class AtorNomeImagemDTO:
    nome: str
    hexadecimal_foto: Optional[str]


@dataclass
class AtorNomeRsDTO:
    nome: str


@dataclass
class AtorEmailRawDTO:
    email: str


@dataclass
class AtorAutorizadoDTO:
    nome: str


@dataclass
class AtorUnidadeDTO:
    id: int
    nome: str


@dataclass
class AtorDadosPesquisaDTO:
    id: int
    nome: str
    data_nascimento: Optional[date]
    hexadecimal_foto: Optional[str]
    data_inicio_intervencao: Optional[date]
    ano_sessao: Optional[str]
    responsavel: Optional[str]
    data_inicio: Optional[date]
    idade: Optional[int]
    par_interacional: Optional[str]
    professor: Optional[str]
    psicologo: Optional[str]
    email_psicologo: Optional[str]
    codigo_psicologo: Optional[int]
    instituicao: Optional[str]
    municipio: Optional[str]
    responsavel_id: Optional[int]
    par_interacional_id: Optional[int]
    professor_id: Optional[int]
    psicologo_id: Optional[int]

    def to_dict(self):
        data_dict = {}
        for field_name in self.__dataclass_fields__.keys():
            value = getattr(self, field_name)
            if isinstance(value, date):
                data_dict[field_name] = value.isoformat()
            elif value is not None:
                data_dict[field_name] = value
        return data_dict


@dataclass
class AtorDadosPesquisaAppDTO:
    responsavel: Optional[str]
    id: int
    foto: Optional[str]
    email: Optional[str]
    profissao: Optional[str]
    tipo: Optional[int]
    vinculo: Optional[str]
    aluno_id: Optional[int]
    sessao: Optional[str]
    titulo: Optional[str]
    aluno: Optional[str]


@dataclass
class AtorAlunoPorResponsavelDTO:
    responsavel: Optional[str]
    id: int
    email: Optional[str]
    telefone_cel: Optional[str]
    aluno_id: Optional[int]


@dataclass
class AtorFilteredGridItemDTO:
    id: int
    nome: str
    idade: Optional[int]
    foto: Optional[str]
    dados_ator: Optional[str]
    modalidade: Optional[str]
    tipo: Optional[str]
    instituicao: Optional[str]
    municipio: Optional[str]
    parecer: Optional[str]
    status: Optional[str]


@dataclass
class AtorGridItemDTO:
    id: int
    dados_ator: Optional[str]
    modalidade: Optional[str]
    tipo: Optional[str]
    instituicao: Optional[str]