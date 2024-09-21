import re

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