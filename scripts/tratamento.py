def obter_tipo_contato_id(cursor, tipo_contato):
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