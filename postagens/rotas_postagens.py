from funcoes_token import token_obrigatorio
from flask import jsonify, request
from funcoes_validacao_dados import validacao_modificacoes_postagem
from funcoes_comandos_sql import adicionar_comandos_sql_postagem
from funcoes_validacao_dados import validar_nova_postagem
from postagens.funcoes_postagens import (obter_postagens, obter_postagem_pelo_autor, obter_postagem_pelo_titulo,
                                         obter_postagem_completa_do_autor, verficar_possivel_titulo_duplicado,
                                         deletar_postagem_pelo_titulo, inserir_nova_postagem)


def configurar_rotas(app):

    @app.route('/postagens', methods=['GET'])
    def obter_postagem():

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:
                postagens = obter_postagens(cursor)
                if not postagens:
                    return jsonify({'mensagem': 'nenhuma postagem encontrada'}), 404

                return jsonify({'Postagens': postagens}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/postagem/titulo/<string:titulo_postagem>', methods=['GET'])
    def obter_postagem_por_titulo(titulo_postagem):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                postagens = obter_postagem_pelo_titulo(titulo_postagem, cursor)
                if not postagens:
                    return jsonify({'mensagem': 'Postagem não encontrada'}), 404

                return jsonify({'postagens': postagens}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/postagem/autor/<string:nome_autor>', methods=['GET'])
    def obter_postagem_de_autor_especifico(nome_autor):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                postagens = obter_postagem_pelo_autor(nome_autor, cursor)
                if not postagens:
                    return jsonify({'mensagem': 'nenhuma postagem encontrada'}), 404

                return jsonify({'postagem': postagens}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/postagem', methods=['POST'])
    @token_obrigatorio
    def nova_postagem(id_autor, perfil):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'autor':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                postagem = request.get_json()
                if not validar_nova_postagem(postagem):
                    return jsonify({'mensagem': 'dados inválidos'}), 400

                titulo = postagem.get('titulo')
                assunto = postagem.get('assunto')

                if verficar_possivel_titulo_duplicado(id_autor, titulo, cursor):
                    return jsonify({'mensagem': 'você já possui uma postagem com esse título!'}), 400

                inserir_nova_postagem(id_autor, titulo, assunto, cursor, app.conexao_bd)
                return jsonify({'mensagem': 'postagem inserida com sucesso.'}), 201

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/postagem/<string:titulo_postagem>', methods=['PUT'])
    @token_obrigatorio
    def editar_postagem(id_autor, perfil, titulo_postagem):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'autor':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                postagem = obter_postagem_completa_do_autor(id_autor, titulo_postagem, cursor)
                if not postagem:
                    return jsonify({'mensagem': 'essa postagem não existe'}), 404

                modificacoes = request.get_json()
                if not validacao_modificacoes_postagem(modificacoes):
                    return jsonify({'mensagem': 'modificações inválidas'}), 400

                partes_sql = []
                valores = []

                adicionar_comandos_sql_postagem(partes_sql, valores, modificacoes, postagem)
                id_postagem = postagem.get('id_postagem')
                valores.append(id_postagem)

                if not partes_sql:
                    return jsonify({'mensagem': "dados repetidos"}), 400

                comando_modificacao = 'update postagens set ' + ', '.join(partes_sql)+' where id_postagem = %s'
                cursor.execute(comando_modificacao, (*valores,))
                app.conexao_bd.commit()

                return jsonify({'mensagem': 'postagem editada com sucesso'}), 201

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500

    @app.route('/postagem/<string:titulo_postagem>', methods=['DELETE'])
    @token_obrigatorio
    def excluir_postagem(id_autor, perfil, titulo_postagem):

        try:
            with app.conexao_bd.cursor(dictionary=True) as cursor:

                if perfil != 'autor':
                    return jsonify({'mensagem': 'acesso restrito'}), 403

                postagem = obter_postagem_completa_do_autor(id_autor, titulo_postagem, cursor)
                if not postagem:
                    return jsonify({'mensagem': 'postagem não encontrada'}), 404

                deletar_postagem_pelo_titulo(id_autor, titulo_postagem, cursor, app.conexao_bd)
                return jsonify({'mensagem': 'postagem excluída com sucesso'}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500
