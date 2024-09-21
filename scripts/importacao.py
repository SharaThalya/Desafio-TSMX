import sys
import os
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.clientes import importar_clientes
from services.cliente_contatos import importar_contatos
from services.cliente_planos import importar_planos
from services.cliente_contratos import importar_contratos
if __name__ == "__main__":
    # Caminho do arquivo Excel na pasta 'data'
    caminho_arquivo_importacao = 'data/dados_importacao.xlsx'

    # Chamar a função de importação
    importar_clientes(caminho_arquivo_importacao)
    # sleep(5)
    importar_planos(caminho_arquivo_importacao)
    # sleep(5)
    importar_contatos(caminho_arquivo_importacao)
    # sleep(5)
    importar_contratos(caminho_arquivo_importacao)