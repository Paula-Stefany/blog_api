import string
import re


def validacao_modificacoes_postagem(modificacoes):

    campos = {
        'titulo': validar_string_nova_postagem,
        'assunto': validar_string_nova_postagem
    }
    for campo, valor in modificacoes.items():
        if campo in campos:
            funcao_validacao = campos[campo]
            if not funcao_validacao(valor):
                return False
    return True


def validacao_modificacoes_autores(modificacoes):

    campos = {
        'nome': validar_nome,
        'email': validar_email,
        'biografia': validar_biografia,
        'senha': validar_senha
    }
    for campo, valor in modificacoes.items():
        if campo in campos:
            funcao_validacao = campos[campo]
            if not funcao_validacao(valor):
                return False
    return True


def validacao_modificacoes_admin(modificacoes):

    campos = {
        'nome':  validar_nome,
        'email': validar_email,
        'senha': validar_senha
    }
    for campo, valor in modificacoes.items():
        if campo in campos:
            funcao_validacao = campos[campo]
            if not funcao_validacao(valor):
                return False
    return True


def validar_novo_autor(novo_autor):

    nome = novo_autor.get('nome')
    email = novo_autor.get('email')
    biografia = novo_autor.get('biografia')
    senha = novo_autor.get('senha')
    return validar_nome(nome) and validar_email(email) and validar_biografia(biografia) and validar_senha(senha)


def validar_administrador(administrador):

    nome = administrador.get('nome')
    email = administrador.get('email')
    senha = administrador.get('senha')
    return validar_nome(nome) and validar_email(email) and validar_senha(senha)


def validar_nova_postagem(postagem):

    titulo = postagem.get('titulo')
    assunto = postagem.get('assunto')
    return validar_string_nova_postagem(titulo) and validar_string_nova_postagem(assunto)


def validar_string_nova_postagem(texto):

    return bool(texto and not texto.isspace())


def validar_nome(nome):

    if not nome or nome[0].isspace() or nome[-1].isspace():
        return False

    return True


def validar_biografia(biografia):

    if not biografia or biografia.isspace():
        return False

    return True


def validar_email(email):

    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


def validar_senha(senha):

    tamanho_senha = 6 <= len(senha) <= 10
    contem_letra = any(caractere.isalpha() for caractere in senha)
    contem_numero = any(caractere.isdigit() for caractere in senha)
    contem_caracter_especial = any(caractere in string.punctuation for caractere in senha)
    contem_espaco = any(caractere.isspace() for caractere in senha)

    return tamanho_senha and contem_letra and contem_numero and contem_caracter_especial and not contem_espaco
