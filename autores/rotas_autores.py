from flask import jsonify, request
from funcoes_token import token_obrigatorio, gerar_token_autor_admin
from funcoes_validacao_dados import validacao_modificacoes_autores, validar_email
from funcoes_comandos_sql import adicionar_comandos_sql_autores
from funcao_enviar_email import enviar_email
from postagens.funcoes_postagens import deletar_todas_postagens_de_um_autor
from autores.funcoes_autores import (obter_dados_basicos_autores, obter_dados_basicos_autor,
                                     obter_dados_completos_autor, deletar_autor)


def configurar_rotas(app):

    @app.route('/autores', methods=['GET'])
    def obter_autores():

        try:

            with app.conexao_bd.cursor(dictionary=True) as cursor:
                autores = obter_dados_basicos_autores(cursor)
                if not autores:
                    return jsonify({'mensagem': 'nenhum autor encontrado'}), 404

                return jsonify({'autores': autores}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/autores/<string:nome_autor>', methods=['GET'])
    def obter_um_autor(nome_autor):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:
                autor = obter_dados_basicos_autor(nome_autor, cursor)
                if not autor:
                    return jsonify({'mensagem': 'autor não encontrado'}), 404

                return jsonify({'autor': autor}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/autores', methods=['POST'])
    @token_obrigatorio
    def novo_autor(id_admin, perfil):

        try:
            if perfil != 'administrador':
                return jsonify({'mensagem': 'acesso restrito'}), 403

            email_novo_autor = request.get_json()
            email = email_novo_autor.get('email')

            if not validar_email(email):
                return jsonify({'mensagem': 'email inválido'}), 400

            token = gerar_token_autor_admin(email)
            convite = f'http://localhost:5050/cadastro_autor?token={token}'
            destinatario = email
            assunto = 'email para cadastro de novo autor'
            conteudo = f'clique no link a seguir para fazer seu cadastro {convite}'

            enviar_email(destinatario, assunto, conteudo)
            return jsonify({'mensagem': 'email enviado com sucesso'}), 200

        except Exception as erro:
            return jsonify({'erro', str(erro)}), 500

    @app.route('/autores/<string:nome_autor>', methods=['PUT'])
    @token_obrigatorio
    def editar_autor(id_autor, perfil, nome_autor):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'autor':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                autor = obter_dados_completos_autor(id_autor, nome_autor, cursor)
                if not autor:
                    return jsonify({'mensagem': 'dados inválidos, voce só pode editar seus próprios dados'}), 400

                modificacoes = request.get_json()
                if not modificacoes:
                    return jsonify({'mensagem': 'Você precisa digitar seus dados'}), 400

                partes_comando_sql = []
                valores = []

                if not validacao_modificacoes_autores(modificacoes):
                    return jsonify({'mensagem': 'dados inválidos'}), 400

                adicionar_comandos_sql_autores(partes_comando_sql, valores, modificacoes, autor, cursor)
                valores.append(id_autor)

                if not partes_comando_sql:
                    return jsonify({'mensagem': 'dados repetidos'}), 400

                comando_modificacao = ('update autores set ' + ', '.join(partes_comando_sql) + ' where id_autor = %s')
                cursor.execute(comando_modificacao, (*valores,))
                app.conexao_bd.commit()

                return jsonify({'mensagem': 'auteração feita com sucesso'}), 201

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/autores/<string:nome_autor>', methods=['DELETE'])
    @token_obrigatorio
    def excluir_autor(id_autor, perfil, nome_autor):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:
                if perfil != 'autor':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                autor = obter_dados_completos_autor(id_autor, nome_autor, cursor)
                if not autor:
                    return jsonify({'mensagem': 'autor não encontrado'}), 404

                deletar_todas_postagens_de_um_autor(id_autor, cursor, app.conexao_bd)

                deletar_autor(id_autor, nome_autor, cursor, app.conexao_bd)
                return jsonify({'mensagem': 'autor excluído com sucesso'}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500
