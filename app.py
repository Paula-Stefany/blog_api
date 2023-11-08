from flask import Flask
from autores.rotas_autores import configurar_rotas as configurar_rotas_autores
from bd import conexao_bd_mysql, close_db_connection
from postagens.rotas_postagens import configurar_rotas as confifurar_rotas_postagem
from login_e_cadastro.rotas_login_e_cadastro import configurar_rotas as configurar_rotas_cadastro_login
from administradores.rotas_administradores import configurar_rotas as configurar_rotas_administradores
from admin_especial.rota_admin_especial import configurar_rotas as configurar_rota_admin_especial


app = Flask(__name__)

app.conexao_bd = conexao_bd_mysql()


configurar_rotas_cadastro_login(app)
configurar_rotas_autores(app)
confifurar_rotas_postagem(app)
configurar_rota_admin_especial(app)
configurar_rotas_administradores(app)

if __name__ == '__main__':

    try:
        app.run(host='localhost', port=5050, debug=True)
    finally:
        close_db_connection(app.conexao_bd)
