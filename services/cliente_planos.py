import pandas as pd
from config.connection import conectar_banco

def importar_planos(arquivo_excel):
    """
    Função para importar dados de planos do arquivo Excel para o PostgreSQL.
    """
    conn = conectar_banco("Iniciando importação de planos...")
    if conn is None:
        return
    cursor = conn.cursor()

    # Ler a planilha Excel
    df = pd.read_excel(arquivo_excel, sheet_name="Planilha2")

    importados = []
    nao_importados = []

    # Iterar sobre as linhas do DataFrame e inserir no banco de dados
    for index, row in df.iterrows():
        try:
            # Extrair o plano e o valor, garantindo a conversão correta do valor
            plano = str(row['Plano']).replace(',', '_').strip()
            valor = round(float(row['Plano Valor']), 2)  # Corrigida a conversão para float e arredondamento

            # Verificar se o plano já existe na tabela tbl_planos
            cursor.execute("SELECT id FROM tbl_planos WHERE descricao = %s", (plano,))
            plano_existente = cursor.fetchone()

            # Se o plano não existir, insira-o
            if not plano_existente:
                cursor.execute("""
                    INSERT INTO tbl_planos (descricao, valor)
                    VALUES (%s, %s)
                """, (plano, valor))
                importados.append(f"Plano importado com sucesso: {plano} - R$ {valor}")

        except Exception as e:
            # Registrar erros e reverter transações em caso de falha
            conn.rollback()
            nao_importados.append(f"Erro ao importar plano {plano}: {e}")
            print(f"Erro ao importar plano {plano}: {e}")

    # Confirmar as inserções no banco de dados
    try:
        conn.commit()
        print(f"{len(importados)} planos importados com sucesso.")
    except Exception as e:
        print(f"Erro ao confirmar transação: {e}")
        conn.rollback()

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

    # Salvar os resultados de importação em arquivos CSV
    pd.DataFrame(importados).to_csv('logs/planos_importados.csv', index=False, encoding='utf-8')
    pd.DataFrame(nao_importados).to_csv('logs/planos_nao_importados.csv', index=False, encoding='utf-8')

    return f"Processo finalizado: {len(importados)} planos importados, {len(nao_importados)} não importados."

