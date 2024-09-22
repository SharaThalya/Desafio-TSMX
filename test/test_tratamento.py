# tests/test_tratamento.py
import pytest
from unittest.mock import MagicMock
from scripts.tratamento import (
    get_tipo_contato_id, verificar_contato_existente, get_status_contrato, 
    get_plano_contrato, obter_uf, contrato_existe, limpar_cep
)


# Testes para a função get_tipo_contato_id
def test_get_tipo_contato_id_existente():
    cursor = MagicMock()
    cursor.fetchone.return_value = [1]
    tipo_contato_id = get_tipo_contato_id(cursor, "Telefone")
    assert tipo_contato_id == 1
    cursor.execute.assert_called_with(
        "SELECT id FROM tbl_tipos_contato WHERE tipo_contato = %s", ("Telefone",)
    )

def test_get_tipo_contato_id_inserir_novo():
    cursor = MagicMock()
    cursor.fetchone.side_effect = [None, [2]]
    tipo_contato_id = get_tipo_contato_id(cursor, "Novo Contato")
    assert tipo_contato_id == 2
    cursor.execute.assert_any_call(
        "INSERT INTO tbl_tipos_contato (tipo_contato) VALUES (%s) RETURNING id", ("Novo Contato",)
    )


# Testes para a função verificar_contato_existente
def test_verificar_contato_existente_true():
    cursor = MagicMock()
    cursor.fetchone.return_value = [1]
    assert verificar_contato_existente(cursor, 1, 1, "+5511987654321") is True

def test_verificar_contato_existente_false():
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    assert verificar_contato_existente(cursor, 1, 1, "+5511987654321") is False


# Testes para a função get_status_contrato
def test_get_status_contrato_existente():
    cursor = MagicMock()
    cursor.fetchone.return_value = [1]
    status_id = get_status_contrato(cursor, "Ativo")
    assert status_id == [1]


# Testes para a função get_plano_contrato
def test_get_plano_contrato_existente():
    cursor = MagicMock()
    cursor.fetchone.return_value = [1]
    plano_id = get_plano_contrato(cursor, "Plano A")
    assert plano_id == [1]


# Testes para a função obter_uf
def test_obter_uf_nome_valido():
    assert obter_uf("São Paulo") == "SP"

def test_obter_uf_sigla_valida():
    assert obter_uf("SP") == "SP"

def test_obter_uf_invalido():
    assert obter_uf("Estado Inexistente") is None


# Testes para a função contrato_existe
def test_contrato_existe_true():
    cursor = MagicMock()
    cursor.fetchone.return_value = [1]
    assert contrato_existe(cursor, "Rua A", "123", "Bairro B", "Cidade C") is True

def test_contrato_existe_false():
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    assert contrato_existe(cursor, "Rua A", "123", "Bairro B", "Cidade C") is False


# Testes para a função limpar_cep
def test_limpar_cep_valido():
    assert limpar_cep("12345-678") == "12345678"

def test_limpar_cep_caracteres_invalidos():
    assert limpar_cep("CEP: 12.345-678") == "12345678"

def test_limpar_cep_invalido():
    assert limpar_cep(None) is None
