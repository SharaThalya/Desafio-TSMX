import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.clientes import importar_clientes
from services.cliente_contatos import importar_contatos
if __name__ == "__main__":
    # Caminho do arquivo Excel na pasta 'data'
    caminho_arquivo_importacao = 'data/dados_importacao.xlsx'

    # Chamar a função de importação
    importar_clientes(caminho_arquivo_importacao)
    importar_contatos(caminho_arquivo_importacao)
