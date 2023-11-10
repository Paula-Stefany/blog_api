from login_e_cadastro.funcoes_login_e_cadastro import (inserir_novo_autor, conferir_dados_login, inserir_novo_admin,
                                                       verificar_se_email_admin_ja_existe_no_banco,
                                                       verificar_se_email_autor_ja_existe_no_banco)
from flask import request, jsonify
from funcoes_token import gerar_token, validar_token
from funcoes_validacao_dados import (validar_administrador, validar_novo_autor)
from funcoes_senha_hash import gerar_senha_hash, gerar_salt


def configurar_rotas(app):

    @app.route('/login', methods=['POST'])
    def login():

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                usuario_inserido = request.get_json()
                email = usuario_inserido.get('email')
                senha = usuario_inserido.get('senha')
                id_usuario, tipo_usuario = conferir_dados_login(email, senha, cursor)

                if id_usuario is None or tipo_usuario is None:
                    return jsonify({'mensagem': 'ceredenciais inválidas'}), 400

                token = gerar_token(id_usuario, tipo_usuario)
                return jsonify({'token': token}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/cadastro_autor', methods=['GET', 'POST'])
    def cadastro_novo_autor():

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                token = request.args.get('token')
                if not token:
                    return jsonify({'mensagem': 'token ausente'}), 404

                resultado, mensagem, token_jwt = validar_token(token)
                if not resultado:
                    return jsonify({'mensagem': mensagem}), 400

                email = token_jwt['email']

                novo_autor = request.get_json()
                if not novo_autor:
                    return {'mensagem': 'voce precisa digitar seus dados'}, 400

                if novo_autor['email'] != email:
                    return jsonify({'mensagem': 'digite o email que voce recebeu o link de convite!'}), 403

                email_presente = verificar_se_email_autor_ja_existe_no_banco(email, cursor)
                if email_presente:
                    return jsonify({'mensagem': 'Autor com esse email já cadastrado'}), 403

                if not validar_novo_autor(novo_autor):
                    return jsonify({'mensagem': 'dados inválidos'}), 400

                salt = gerar_salt()
                senha_hash = gerar_senha_hash(novo_autor.get('senha'), salt)
                inserir_novo_autor(novo_autor['nome'], novo_autor['email'], novo_autor['biografia'],
                                   salt, senha_hash, cursor, app.conexao_bd)

                return jsonify({'mensagem': 'autor inserido com sucesso'}), 201

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/cadastro_admin', methods=['GET', 'POST'])
    def registrar_novo_admin():

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                token = request.args.get('token')
                if not token:
                    return jsonify({'mensagem": "token ausente'}), 404

                resultado, mensagem, token_jwt = validar_token(token)
                if not resultado:
                    return jsonify({'mensagem': mensagem}), 400

                email = token_jwt['email']

                novo_admin = request.get_json()
                if not novo_admin:
                    return jsonify({'mensagem': 'Voce precisa digitar seus dados'}), 400

                if novo_admin['email'] != email:
                    return jsonify({'mensagem': 'digite o email que você recebeu o link de convite.'}), 403

                email_presente = verificar_se_email_admin_ja_existe_no_banco(email, cursor)
                if email_presente:
                    return jsonify({'mensagem': 'administrador com esse email já cadastrado'}), 400

                if not validar_administrador(novo_admin):
                    return jsonify({'mensagem': 'dados inválidos'}), 400

                salt = gerar_salt()
                senha_hash = gerar_senha_hash(novo_admin['senha'], salt)
                inserir_novo_admin(novo_admin['nome'], novo_admin['email'], salt, senha_hash, cursor, app.conexao_bd)

                return jsonify({'mensagem': 'Novo administrador cadastrado com sucesso!'}), 201

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500
