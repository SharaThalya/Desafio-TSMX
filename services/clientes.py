import pandas as pd
from config.connection import conectar_banco
from scripts.validacao import extrair_cpf_cnpj

def importar_clientes(arquivo_excel):
    """
    Função para importar dados de clientes do arquivo Excel para o PostgreSQL.
    """
    conn = conectar_banco("Iniciando importação de clientes...")
    if conn is None:
        return
    
    cursor = conn.cursor()

    df = pd.read_excel(arquivo_excel, sheet_name='Planilha2')
    
    importados = []
    nao_importados = []
    contadorImportacoes = 0
    contadorNaoImportados = 0

    for index, row in df.iterrows():
        try:
            cpfCnpj = extrair_cpf_cnpj(str(row['CPF/CNPJ']))
            cursor.execute("SELECT id FROM tbl_clientes WHERE cpf_cnpj = %s", (cpfCnpj,))
            cliente_existente = cursor.fetchone()

            if cliente_existente:
                contadorNaoImportados += 1
                # print(f"Cliente já existe: {cpfCnpj} - {row['Nome/Razão Social']}")
                nao_importados.append(f"Cliente já existe: {cpfCnpj} - {row['Nome/Razão Social']}")
                continue

            data_nascimento = row['Data Nasc.'] if pd.notna(row['Data Nasc.']) else None
            data_cadastro = row['Data Cadastro cliente'] if pd.notna(row['Data Cadastro cliente']) else None

            cursor.execute("""
                INSERT INTO tbl_clientes (nome_razao_social, nome_fantasia, cpf_cnpj, data_nascimento, data_cadastro)
                VALUES (%s, %s, %s, %s, %s)
                """, 
                (
                    row['Nome/Razão Social'], 
                    row['Nome Fantasia'] if pd.notna(row['Nome Fantasia']) else None,  # Tratar valores NaN
                    cpfCnpj,
                    data_nascimento, 
                    data_cadastro
                )
            )
            contadorImportacoes += 1
            # print(f"Cliente importado com sucesso: {row['Nome/Razão Social']}")
            importados.append(f"Cliente importado com sucesso: {row['Nome/Razão Social']}") 
        
        except Exception as e:
            contadorNaoImportados += 1
            print(f"Erro ao importar cliente {row['Nome/Razão Social']}: {e}")
            nao_importados.append(f"Erro ao importar cliente {row['Nome/Razão Social']}: {e}") 
            conn.rollback()
            continue


    try:
        conn.commit()
    except Exception as e:
        print(f"Erro ao confirmar transação: {e}")
        conn.rollback() 

    cursor.close()
    conn.close()
    
    pd.DataFrame(importados).to_csv('logs/clientes_importados.csv', index=True, encoding='utf-8')
    pd.DataFrame(nao_importados).to_csv('logs/clientes_nao_importados.csv', index=True, encoding='utf-8')
    
    print(f"Processo finalizado: {len(importados)} clientes importados, {len(nao_importados)} clientes não importados.")