import pandas as pd
import re


def get_tipo_contato_id(cursor, tipo_contato):
    """
    Função para obter o ID do tipo de contato. Se o tipo de contato não existir,
    ele será inserido na tabela tbl_tipo_contato.
    """
    cursor.execute("SELECT id FROM tbl_tipos_contato WHERE tipo_contato = %s", (tipo_contato,))
    resultado = cursor.fetchone()
    
    if resultado:
        return resultado[0]
    else:
        cursor.execute("INSERT INTO tbl_tipos_contato (tipo_contato) VALUES (%s) RETURNING id", (tipo_contato,))
        tipo_contato_id = cursor.fetchone()[0]
        return tipo_contato_id
    
    
def verificar_contato_existente(cursor, cliente_id, tipo_contato_id, contato):
    """
    Verifica se o contato já existe na tabela tbl_cliente_contatos.
    """
    cursor.execute("""
        SELECT 1 FROM tbl_cliente_contatos
        WHERE cliente_id = %s AND tipo_contato_id = %s AND contato = %s
    """, (cliente_id, tipo_contato_id, contato))
    
    return cursor.fetchone() is not None


def get_status_contrato(cursor, status):
    cursor.execute("""SELECT tc.id FROM tbl_status_contrato tc
                   WHERE %s = tc.status
                   """,
                   (status,))
    status = cursor.fetchone()
    
    return status

def get_plano_contrato(cursor, plano):
    cursor.execute("""
                   SELECT tp.id FROM tbl_planos tp
                   WHERE tp.descricao = %s 
                   """, (plano,))
    plano = cursor.fetchone()
    
    return plano

import pandas as pd

def obter_uf(uf):
    """
    Função para converter o nome do estado para a sigla correta.
    Aceita o nome completo do estado ou a sigla e retorna a sigla.
    """
    # Dicionário para mapear os nomes dos estados para suas respectivas siglas
    ESTADOS_MAP = {
        'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA',
        'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
        'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
        'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI',
        'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS',
        'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC', 'São Paulo': 'SP',
        'Sergipe': 'SE', 'Tocantins': 'TO'
    }

    # Verifica se a entrada não é NaN e faz a conversão para string, removendo espaços desnecessários
    if pd.notna(uf):
        uf = str(uf)

        # Tenta converter o nome do estado para a sigla
        if uf in ESTADOS_MAP:
            return ESTADOS_MAP[uf]
        
        # Se já estiver no formato de sigla e for válido, retorna como está
        if len(uf) == 2 and uf.upper() in ESTADOS_MAP.values():
            return uf.upper()

    # Retorna None se não for possível mapear para uma sigla válida
    return None


def contrato_existe(cursor, logradouro, numero, bairro, cidade):
    """
    Função para verificar se um contrato já existe na tabela tbl_cliente_contratos.
    A verificação é feita com base no endereço completo, independentemente do cliente e plano.
    """
    cursor.execute("""
        SELECT id FROM tbl_cliente_contratos
        WHERE endereco_logradouro = %s AND endereco_numero = %s
        AND endereco_bairro = %s AND endereco_cidade = %s
    """, (logradouro, numero, bairro, cidade))
    return cursor.fetchone() is not None


def limpar_cep(cep):
    """
    Função para limpar o CEP, removendo todos os caracteres que não sejam números.
    """
    if pd.notna(cep):
        # Remove qualquer caractere que não seja número
        return re.sub(r'\D', '', str(cep))
    return None