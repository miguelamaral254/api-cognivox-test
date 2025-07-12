from datetime import datetime, date 
def validate_ator_data(data, is_update=False):
    required_fields = ['nome', 'email', 'profissao_id', 'unidade_id', 'status']
    
    if not is_update:
        required_fields.extend(['data_nascimento', 'senha', 'usuario'])
        
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Campo obrigatório '{field}' ausente ou vazio."

    if 'email' in data and '@' not in data['email']:
        return False, "Formato de e-mail inválido."

    for field in ['profissao_id', 'unidade_id', 'idioma_id', 'modalidade_ensino_id', 'status']:
        if field in data and data[field] not in [None, '']:
            try:
                data[field] = int(data[field])
            except ValueError:
                return False, f"Campo '{field}' deve ser um número inteiro válido."

    for field in ['data_nascimento', 'data_inicio_intervencao']:
        if field in data and data[field] not in [None, '']:
            try:
                if isinstance(data[field], str):
                    data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
            except ValueError:
                return False, f"Campo de data '{field}' com formato inválido. Use YYYY-MM-DD."

    if 'nome' in data and len(data['nome']) > 255:
        return False, "Nome muito longo."
    
    return True, None

def validate_vinculo_data(data):
    required_fields = ['NOMER', 'EMAILR', 'TELEFONECEL', 'TIPO_VINCULO', 'UNIDADEID']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Campo obrigatório de vínculo '{field}' ausente ou vazio."
    return True, None