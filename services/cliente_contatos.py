import pandas as pd
from config.connection import conectar_banco
from scripts.validacao import formatar_telefone, validar_email, extrair_cpf_cnpj
from scripts.tratamento import get_tipo_contato_id, verificar_contato_existente


def importar_contatos(arquivo_excel):
    """
    Função para importar dados de contatos do arquivo Excel para o PostgreSQL.
    """
    conn = conectar_banco("Iniciando importação de contatos...")
    if conn is None:
        return
    
    cursor = conn.cursor()

    # Ler a planilha Excel
    df = pd.read_excel(arquivo_excel, sheet_name='Planilha2')
  
    importados = []
    nao_importados = []
    contadorImportacoes = 0
    contadorNaoImportados = 0

    # Iterar sobre as linhas do DataFrame e inserir no banco de dados
    for index, row in df.iterrows():
        try:
            # Verificar se o cliente já existe (baseado no CPF/CNPJ)
            cpfCnpj = extrair_cpf_cnpj(str(row['CPF/CNPJ']))
            cursor.execute("SELECT id FROM tbl_clientes WHERE cpf_cnpj = %s", (cpfCnpj,))
            cliente_existente = cursor.fetchone()

            if not cliente_existente:
                contadorNaoImportados += 1
                print(f"Cliente não encontrado para o contato: {cpfCnpj} - {row['Nome/Razão Social']}")
                nao_importados.append(f"Cliente não encontrado: {cpfCnpj} - {row['Nome/Razão Social']}")
                continue

            cliente_id = cliente_existente[0]

            # Tipos de contato e seus respectivos valores
            contatos = [
                ('Telefone', formatar_telefone(row['Telefones'], tipo='fixo') if pd.notna(row['Telefones']) else None),
                ('Celular', formatar_telefone(row['Celulares'], tipo='celular') if pd.notna(row['Celulares']) else None),
                ('E-Mail', row['Emails'] if pd.notna(row['Emails']) and validar_email(row['Emails']) else None)
            ]

            # Inserir cada tipo de contato na tabela tbl_cliente_contatos
            for tipo_contato, valor_contato in contatos:
                if valor_contato is None:
                    # Registrar o contato nulo como não importado
                    contadorNaoImportados += 1
                    nao_importados.append(f"Contato ({tipo_contato}) nulo para {row['Nome/Razão Social']}")
                    continue

                # Obter ou inserir o tipo de contato na tbl_tipo_contato
                tipo_contato_id = get_tipo_contato_id(cursor, tipo_contato)
                
                contato_existe = verificar_contato_existente(cursor, cliente_id, tipo_contato_id, valor_contato)

                if not contato_existe:
                    # Inserir o contato na tbl_cliente_contatos
                    cursor.execute("""
                        INSERT INTO tbl_cliente_contatos (cliente_id, tipo_contato_id, contato)
                        VALUES (%s, %s, %s)
                    """, 
                    (
                        cliente_id,
                        tipo_contato_id,
                        valor_contato
                    ))
                    contadorImportacoes += 1
                    importados.append(f"Contato ({tipo_contato}) importado com sucesso: {row['Nome/Razão Social']} - {valor_contato}")
                else:
                    contadorNaoImportados += 1
                    nao_importados.append(f"Contato ({tipo_contato}) já existe para {row['Nome/Razão Social']}: {valor_contato}") 
        
        except Exception as e:
            contadorNaoImportados += 1
            print(f"Erro ao importar contato {row['Nome/Razão Social']}: {e}")
            nao_importados.append(f"Erro ao importar contato {row['Nome/Razão Social']}: {e}") 
            conn.rollback()  # Reverter a transação em caso de erro
            continue

    try:
        conn.commit()
    except Exception as e:
        print(f"Erro ao confirmar transação: {e}")
        conn.rollback() 

    cursor.close()
    conn.close()
    
    pd.DataFrame(importados).to_csv('logs/contatos_importados.csv', index=True, encoding='utf-8')
    pd.DataFrame(nao_importados).to_csv('logs/contatos_nao_importados.csv', index=True, encoding='utf-8')
    
    return f"""
Processo finalizado. Arquivos CSV gerados.
{contadorImportacoes} registros de contato importados!
{contadorNaoImportados} registros de contato não importados!
          """
