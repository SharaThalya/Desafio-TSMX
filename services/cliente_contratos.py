import pandas as pd
from config.connection import conectar_banco
from scripts.validacao import extrair_cpf_cnpj
from scripts.tratamento import get_status_contrato, get_plano_contrato, obter_uf, contrato_existe, limpar_cep


def importar_contratos(arquivo_excel):
    conn = conectar_banco("Iniciando importação de contratos...")
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
            # Extrair o CPF/CNPJ e verificar a existência do cliente
            cpfCnpj = extrair_cpf_cnpj(str(row['CPF/CNPJ']))
            cursor.execute("SELECT id FROM tbl_clientes WHERE cpf_cnpj = %s", (cpfCnpj,))
            cliente_existente = cursor.fetchone()
            
            if not cliente_existente:
                contadorNaoImportados += 1
                print(f"Cliente não encontrado para o contrato: {cpfCnpj} - {row['Nome/Razão Social']}")
                nao_importados.append(f"Cliente não encontrado para o contrato: {cpfCnpj} - {row['Nome/Razão Social']}")
                continue
            
            cliente_id = cliente_existente[0]

            # Verificação do campo Isento
            isento = True if pd.notna(row['Isento']) and str(row['Isento']).strip() != '' else False

            # Obter os IDs de status do contrato e plano
            status_contrato_id = get_status_contrato(cursor, row['Status'])
            plano = str(row['Plano']).replace(',', '_').strip()
            plano_id = get_plano_contrato(cursor, plano)
            vencimento = int(row['Vencimento']) if pd.notna(row['Vencimento']) else None
            uf = str(obter_uf(row['UF']))
            cep = str(limpar_cep(row['CEP']))
            logradouro = str(row['Endereço'])
            numero = str(row['Número'])
            bairro = str(row['Bairro'])
            cidade = str(row['Cidade'])
            complemento = str(row['Complemento']) if pd.notna(row['Complemento']) else None
            desconto = float(row['Desconto']) if pd.notna(row['Desconto']) else 0.0
            mac = str(row['MAC']).strip() if pd.notna(row['MAC']) else None
            ip = str(row['IP']).strip() if pd.notna(row['IP']) else None

            # Verificar se o contrato já existe para evitar duplicidade com base no endereço
            if contrato_existe(cursor, logradouro, numero, bairro, cidade):
                contadorNaoImportados += 1
                nao_importados.append(f"Contrato duplicado para o endereço: {logradouro}, {numero} - {row['Nome/Razão Social']}")
                continue

            # Inserir o contrato na tabela tbl_cliente_contratos
            cursor.execute("""
                INSERT INTO tbl_cliente_contratos (
                    cliente_id, 
                    plano_id,
                    dia_vencimento,
                    isento,
                    endereco_logradouro,
                    endereco_numero,
                    endereco_bairro,
                    endereco_cidade,
                    endereco_complemento,
                    endereco_cep,
                    endereco_uf,
                    status_id,
                    desconto,
                    mac,
                    ip
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
                """, (
                    cliente_id,
                    plano_id,
                    vencimento,
                    isento,
                    logradouro,
                    numero,
                    bairro,
                    cidade,
                    complemento,
                    cep,
                    uf,
                    status_contrato_id,
                    desconto,
                    mac,
                    ip,
                ))
            importados.append(f"Contrato importado com sucesso para {row['Nome/Razão Social']}!")
            contadorImportacoes += 1

        except Exception as e:
            conn.rollback()
            contadorNaoImportados += 1
            nao_importados.append(f"Erro ao importar contrato para {row['Nome/Razão Social']}. {e}")
            print(f"Erro ao importar contrato para {row['Nome/Razão Social']}: {e}")
            
    # Confirmação da transação
    try:
        conn.commit()
        print(f"{contadorImportacoes} contratos importados com sucesso!")
    except Exception as e:
        print(f"Erro ao confirmar transação: {e}")
        conn.rollback()
        
    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()
    
    # Salvar os resultados de importação em arquivos CSV
    pd.DataFrame(importados).to_csv('logs/contratos_importados.csv', index=False, encoding='utf-8')
    pd.DataFrame(nao_importados).to_csv('logs/contratos_nao_importados.csv', index=False, encoding='utf-8')

    print(f"Processo finalizado: {contadorImportacoes} contratos importados, {contadorNaoImportados} contratos não importados.")