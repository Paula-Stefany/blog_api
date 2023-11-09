from funcoes_validacao_dados import validar_email
from flask import jsonify, request
from funcoes_token import gerar_token_autor_admin
from funcao_enviar_email import enviar_email


def configurar_rotas(app):

    @app.route('/admin_especial', methods=['POST'])
    def inserir_admin_especial():

        """ A idéia dessa rota é usá-la apenas 1 vez, no caso, quando inserirmos o administrador especial, e depois
         excluí-la ou deixá-la comentada. Também pegaremos o email do administrador especial e colocaremos no arquivo
         .env manualmente ex: EMAIL_ADMIN_ESPECIAL = 'email do admin especial'  porque será a forma que identificaremos
         o administrador especial dentro da tabela administradores que contém o email como sendo unique """

        try:

            administrador_especial = request.get_json()
            email_administrador_especial = administrador_especial.get('email')

            if not email_administrador_especial:
                return jsonify({'mensagem': 'email não encontrado!'}), 404

            if not validar_email(email_administrador_especial):
                return jsonify({'mensagem': 'Email inválido'}), 400

            token = gerar_token_autor_admin(email_administrador_especial)
            convite = f'http://localhost:5050/cadastro_admin?token={token}'
            destinatario = email_administrador_especial
            assunto = 'email de cadastro'
            conteudo = f'acesse o link a seguir para fazer seu cadastro como administrador {convite}'

            enviar_email(destinatario, assunto, conteudo)

            return jsonify({'mensagem': 'email enviado com sucesso!'}), 200

        except Exception as erro:
            return jsonify({'erro': str(erro)}), 500
