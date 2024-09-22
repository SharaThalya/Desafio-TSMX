from scripts.validacao import extrair_cpf_cnpj, formatar_telefone, validar_email

# Testes para a função extrair_cpf_cnpj
def test_extrair_cpf_valido():
    assert extrair_cpf_cnpj('Meu CPF é 123.456.789-00.') == '12345678900'

def test_extrair_cnpj_valido():
    assert extrair_cpf_cnpj('Empresa com CNPJ 12.345.678/0001-90.') == '12345678000190'

def test_extrair_cpf_invalido():
    # Teste com string que não contém um CPF válido
    assert extrair_cpf_cnpj('CPF inválido 123.45.67-890') == 'CPF inválido 123.45.67-890'

def test_extrair_cnpj_invalido():
    # Teste com string que não contém um CNPJ válido
    assert extrair_cpf_cnpj('CNPJ inválido 12.3456.7890/0001-99') == 'CNPJ inválido 12.3456.7890/0001-99'

def test_extrair_cpf_cnpj_misturados():
    # Teste com uma string contendo tanto CPF quanto CNPJ
    assert extrair_cpf_cnpj('Meu CPF é 123.456.789-00 e meu CNPJ é 12.345.678/0001-90.') == '12345678900'

def test_extrair_cpf_cnpj_formatos_incomuns():
    # Teste com formatos incomuns de CPF/CNPJ que devem ser ignorados
    assert extrair_cpf_cnpj('CPF: 123-456.789/00') == 'CPF: 123-456.789/00'

# Testes para a função formatar_telefone
def test_formatar_telefone_fixo_valido():
    assert formatar_telefone('551132165432', tipo='fixo') == '+55 11 3216-5432'

def test_formatar_telefone_celular_valido():
    assert formatar_telefone('5511987654321', tipo='celular') == '+55 11 98765-4321'

def test_formatar_telefone_invalido():
    # Teste com número de telefone inválido
    assert formatar_telefone('1234') is None

def test_formatar_telefone_caracteres_invalidos():
    # Teste com caracteres não numéricos
    assert formatar_telefone('telefone inválido 5511987654321') is None

def test_formatar_telefone_vazio():
    # Teste com uma string vazia
    assert formatar_telefone('') is None

def test_formatar_telefone_apenas_espacos():
    # Teste com uma string de espaços
    assert formatar_telefone('   ') is None

def test_formatar_telefone_tamanho_excessivo():
    # Teste com um número muito longo
    assert formatar_telefone('551198765432123456789') is None

def test_formatar_telefone_formatos_estranhos():
    # Teste com formatos não convencionais de número
    assert formatar_telefone('+55-11-98765-4321') is None
    assert formatar_telefone('55(11)987654321') is None

# Testes para a função validar_email
def test_validar_email_valido():
    assert validar_email('teste@example.com') is True

def test_validar_email_invalido():
    assert validar_email('emailinvalido@@example..com') is False

def test_validar_email_com_caracteres_especiais():
    assert validar_email('user.name+tag+sorting@example.com') is True

def test_validar_email_espacos():
    # Teste de email com espaços, que deve ser inválido
    assert validar_email(' user@example.com ') is False

def test_validar_email_faltando_dominio():
    # Teste com email faltando o domínio
    assert validar_email('username@.com') is False

def test_validar_email_faltando_usuario():
    # Teste com email faltando o usuário antes do @
    assert validar_email('@example.com') is False

def test_validar_email_vazio():
    # Teste com string vazia
    assert validar_email('') is False

def test_validar_email_apenas_espacos():
    # Teste com uma string contendo apenas espaços
    assert validar_email('   ') is False

def test_validar_email_acentuado():
    # Teste com email acentuado, que normalmente é considerado inválido
    assert validar_email('usuário@exemplo.com') is False
