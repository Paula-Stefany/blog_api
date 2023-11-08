import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
usuario_mysql = os.getenv('USUARIO_MYSQL')
senha_mysql = os.getenv('SENHA_MYSQL')


def conexao_bd_mysql():

    return mysql.connector.connect(
        host='localhost',
        user=usuario_mysql,
        password=senha_mysql,
        database='blog'
    )


def close_db_connection(conexao):

    if conexao:
        conexao.close()
