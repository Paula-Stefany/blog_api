from flask import request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()
chave_secreta = os.getenv('CHAVE_SECRETA')


def gerar_token(id_usuario, tipo_usuario):

    expiracao = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({'tipo_usuario': tipo_usuario, 'id_usuario': id_usuario, 'exp': expiracao}, chave_secreta,
                       algorithm="HS256")
    return token


def validar_token(jwt_token):

    try:
        token_jwt = jwt.decode(jwt_token, chave_secreta, algorithms="HS256")
        return True, 'token válido', token_jwt

    except jwt.ExpiredSignatureError:
        return False, 'token expirado', None

    except jwt.InvalidTokenError:
        return False, 'token inválido', None


def obter_token():

    token_fornecido = request.headers.get('Authorization')
    if not token_fornecido:
        return None

    jwt_token = retirar_headers_do_token(token_fornecido)
    return jwt_token


def retirar_headers_do_token(token):

    token_dividido = token.split()
    if len(token_dividido) != 2 or token_dividido[0].lower() != 'bearer':
        return None
    token_jwt = token_dividido.pop(1)
    return token_jwt


def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = obter_token()
        if not token:
            return jsonify({"mensagem": "token de acesso ausente"}), 401

        valido, mensagem, token_jwt = validar_token(token)

        if valido:
            id_usuario = token_jwt['id_usuario']
            tipo_usuario = token_jwt['tipo_usuario']
            return f(id_usuario, tipo_usuario, *args, **kwargs)

        else:
            return jsonify({"mensagem": mensagem}), 401

    return decorated


def gerar_token_autor_admin(email):

    expiracao = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({'email': email, 'exp': expiracao}, chave_secreta, algorithm="HS256")
    return token
