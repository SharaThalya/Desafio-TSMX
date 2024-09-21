import pandas as pd
from config.connection import conectar_banco


def importar_tipos_contato(arquivo_excel):
    
    
    conn = conectar_banco()
    if conn is None:
        return
    
    cursor = conn.cursor()
    
    df = pd.read_excel(arquivo_excel, sheet_name='Planilha2')
    index = 0
    for column in df.columns:
        index +=1
        try:
            if index in (6, 7, 8):
                cursor.execute("SELECT id FROM tbl_tipos_contato WHERE tipo_contato = %s", df.columns[index])
                tipo_contato_existente = cursor.fetchone()
            if tipo_contato_existente:
                continue
            
            cursor.execute("""
                           INSERT INTO tbl_tipos_contato (tipo_contato)
                           VALUES (%s)
                           """,
                           (
                               df.columns[5]
                           )
                           )