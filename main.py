import pandas as pd
import psycopg2 


conn = psycopg2.connect(
    host="localhost",
    dbname="db_des_tsmx",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

df = pd.read_excel("C:/Users/jluca/Downloads/dados_importacao.xlsx", engine="openpyxl")
