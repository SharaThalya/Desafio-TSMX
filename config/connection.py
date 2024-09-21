import psycopg2

# Função para conectar ao banco
def conectar_banco():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="db_des_tsmx",
            user="postgres",
            password="postgres" 
        )
        print("Conectado ao banco de dados com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None