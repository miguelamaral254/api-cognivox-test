INSERT INTO cognvox.ator (
    id, nome, cpf, ano_sessao, data_nascimento, data_inicio_intervencao, 
    reg_profissional, email, telefone_cel, telefone_fixo, idioma_id, 
    unidade_id, profissao_id, endereco, cidade, estado, pais, 
    hexadecimal_foto, modalidade_ensino_id, status
) VALUES (
    9999, 'Admin', '000.000.000-00', '2025', CURDATE(), CURDATE(),
    'REG-ADMIN', 'admin@cognivox.com.br', '00000000000', '0000000000', 1,
    23,
    100,
    'Endereço Admin', 'Recife', 'PE', 'Brasil',
    '/src/assets/temp/179FOTOMARKETING.jpg',
    40,
    1
) ON DUPLICATE KEY UPDATE nome='Admin';

INSERT INTO cognvox.usuario1 (
    codigo, usuario, senha, cod_empresa, nome, email, cod_status, 
    cod_grupo_usuario, cod_nivel, primeiro_acesso, erros_login, ator_id
) VALUES (
    1, 
    'admin', 
    'YWRtaW4=', 
    23,  
    'Administrador do Sistema', 
    'admin@cognvox.com.br', 
    1, 
    1, 
    1, 
    0, 
    0, 
    9999 
) ON DUPLICATE KEY UPDATE usuario='admin';