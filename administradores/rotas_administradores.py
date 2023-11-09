from funcoes_token import token_obrigatorio, gerar_token_autor_admin
from flask import request, jsonify
from postagens.funcoes_postagens import (deletar_postagem_pelo_id_postagem, deletar_todas_postagens_de_um_autor,
                                         obter_postagem_pelo_id_postagem)
from funcao_enviar_email import enviar_email
from funcoes_validacao_dados import validacao_modificacoes_admin, validar_email
from funcoes_comandos_sql import adicionar_comandos_sql_admins
import os
from dotenv import load_dotenv
from autores.funcoes_autores import verificar_existencia_do_autor, deletar_autor_pelo_id
from administradores.funcoes_admin import (obter_historico_autor, verificar_admin_especial, obter_dados_admin_unico,
                                           obter_dados_administradores, verificar_permicao_administrador,
                                           obter_dados_basicos_admin, deletar_administrador)


load_dotenv()
email_admin_especial = os.getenv('EMAIL_ADMIN_ESPECIAL')


def configurar_rotas(app):

    @app.route('/admins', methods=['GET'])
    @token_obrigatorio
    def vizualizar_admins(id_admin, perfil):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso negado'}), 403

                admin_especial = verificar_admin_especial(id_admin, email_admin_especial, cursor)
                if not admin_especial:
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                administradores = obter_dados_administradores(cursor)

                return jsonify({'administradores': administradores}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/admin/<string:nome_admin>', methods=['GET'])
    @token_obrigatorio
    def visualizar_unico_admin(id_admin, perfil, nome_admin):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso negado'}), 403

                admin_especial = verificar_admin_especial(id_admin, email_admin_especial, cursor)
                if not admin_especial:
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                dados_admin = obter_dados_admin_unico(nome_admin, cursor)
                if not dados_admin:
                    return jsonify({'mensagem': 'administrador não encontrado!'}), 404

                return jsonify({'administrador': dados_admin}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/historico_autor/<string:nome_autor>', methods=['GET'])
    @token_obrigatorio
    def obtendo_historico_autor_postagem(id_admin, perfil, nome_autor):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso negado'}), 403

                historico_autor = obter_historico_autor(nome_autor, cursor)
                if not historico_autor:
                    return jsonify({'mensagem': 'autor não encontrado'}), 404

                return jsonify({'histórico': historico_autor}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/admin', methods=['POST'])
    @token_obrigatorio
    def adicionar_admin(id_admin, perfil):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso negado'}), 403

                administrador = verificar_admin_especial(id_admin, email_admin_especial, cursor)
                if not administrador:
                    return jsonify({'mensagem': 'acesso restrito!'}), 403

                novo_administrador_email = request.get_json()
                email_novo_admin = novo_administrador_email .get('email')

                if not validar_email(email_novo_admin):
                    return jsonify({'mensagem': 'dados inválidos'}), 400

                token = gerar_token_autor_admin(email_novo_admin)
                convite = f'http://localhost:5050/cadastro_admin?token={token}'
                destinatario = email_novo_admin
                assunto = 'email para cadastro de novo administrador'
                conteudo = f'Acesse esse link para fazer seu cadastro como novo administrador: {convite}'

                enviar_email(destinatario, assunto, conteudo)

                return jsonify({'mensagem': "email enviado com sucesso"}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/admin/<string:nome_admin>', methods=['PUT'])
    @token_obrigatorio
    def editar_dados(id_admin, perfil, nome_admin):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso negado'}), 403

                administrador = verificar_permicao_administrador(id_admin, nome_admin, cursor)
                if not administrador:
                    return jsonify({'mensagem': 'Acesso negado'}), 403

                modificacoes = request.get_json()
                if not modificacoes:
                    return jsonify({'mensagem': 'voce precisa digitar os dados'}), 400

                if not validacao_modificacoes_admin(modificacoes):
                    return jsonify({'mensagem': 'dados inválidos'}), 400

                partes_sql = []
                valores = []

                adicionar_comandos_sql_admins(partes_sql, valores, modificacoes, administrador, cursor)
                if not partes_sql:
                    return jsonify({"mensagem": "dados repetidos"}), 400

                valores.append(id_admin)

                comando_modificacao = ('update administradores set '+', '.join(partes_sql) + ' where id_admin = %s'
                                                                                             ' and nome = %s;')
                cursor.execute(comando_modificacao, (*valores, nome_admin))
                app.conexao_bd.commit()

                return jsonify({'mensagem': 'modificações feitas com sucesso'}), 201

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/admin/<string:nome_admin>/', methods=['DELETE'])
    @token_obrigatorio
    def excluir_admin(id_admin, perfil, nome_admin):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso negado'}), 403

                administrador_especial = verificar_admin_especial(id_admin, email_admin_especial, cursor)
                if not administrador_especial:
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                admin_a_ser_exluido = obter_dados_basicos_admin(nome_admin, cursor)
                if not admin_a_ser_exluido:
                    return jsonify({'mensagem': 'administrador não encontrado'}), 404

                deletar_administrador(nome_admin, cursor, app.conexao_bd)

                return jsonify({'mensagem': 'administrador excluído com sucesso'}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/admin/excluir_autor/<int:id_autor>', methods=['DELETE'])
    @token_obrigatorio
    def excluir_um_autor(id_admin, perfil, id_autor):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                autor = verificar_existencia_do_autor(id_autor, cursor)
                if not autor:
                    return jsonify({"mensagem": "autor não encontrado"}), 404

                deletar_todas_postagens_de_um_autor(id_autor, cursor, app.conexao_bd)
                deletar_autor_pelo_id(id_autor, cursor, app.conexao_bd)

                return jsonify({'mensagem': 'autor excluído com sucesso!'}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/admin/excluir_postagem/<int:id_postagem>', methods=['DELETE'])
    @token_obrigatorio
    def excluir_uma_postagem(id_admin, perfil, id_postagem):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'administrador':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                postagem = obter_postagem_pelo_id_postagem(id_postagem, cursor)
                if not postagem:
                    return jsonify({"mensagem": "postagem não encontrada"}), 404

                deletar_postagem_pelo_id_postagem(id_postagem, cursor, app.conexao_bd)
                return jsonify({'mensagem': 'postagem excluída com sucesso'}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500
