import re
from phonenumbers import NumberParseException
from phonenumbers import NumberParseException, is_valid_number, parse, format_number, PhoneNumberFormat


def extrair_cpf_cnpj(cpfCnpj):
    """
    Extrai CPF ou CNPJ de um texto, removendo pontos, traços e barras.
    Retorna o número como uma string contendo apenas os dígitos.
    """
    # Expressões regulares para CPF (11 dígitos) e CNPJ (14 dígitos)
    regex_cpf = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
    regex_cnpj = r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b'
    
    # Procurar por CPF no texto
    cpf_encontrado = re.search(regex_cpf, cpfCnpj)
    if cpf_encontrado:
        # Remover os caracteres especiais do CPF
        return re.sub(r'\D', '', cpf_encontrado.group())
    
    # Procurar por CNPJ no texto
    cnpj_encontrado = re.search(regex_cnpj, cpfCnpj)
    if cnpj_encontrado:
        # Remover os caracteres especiais do CNPJ
        return re.sub(r'\D', '', cnpj_encontrado.group())
    
    return cpfCnpj



def formatar_telefone(telefone, tipo='fixo'):
    """
    Função para formatar números de telefone e celular.
    Formato esperado: +XX XXXXX-XXXX para celular e +XX XXXX-XXXX para fixo.
    """
    if telefone is None:
        return None
    try:
        telefone_str = str(int(float(telefone)))  # Converter para string, tratando como número sem decimais
        telefone_parsed = parse(telefone_str, "BR")

        # Verificar se o número é válido
        if not is_valid_number(telefone_parsed):
            return "INVÁLIDO!"

        # Formatar o número no formato internacional
        return format_number(telefone_parsed, PhoneNumberFormat.INTERNATIONAL)

    except (ValueError, NumberParseException):
        return None  # Retorna None se o telefone não puder ser formatado corretamente

    
def validar_email(email):
    """
    Função para validar o formato do email usando regex.
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    return False