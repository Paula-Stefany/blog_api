from funcoes_senha_hash import (verificar_senha_fornecida_pelo_autor, obter_senha_hash_original_autor,
                                verificar_senha_fornecida_pelo_admin, obter_senha_hash_original_admin)


def verificar_igualdade_dados_autor(campo_bd, valor_modificado, autor_atual, cursor):

    if campo_bd == 'senha':

        senha = valor_modificado
        senha_hash_fornecida = verificar_senha_fornecida_pelo_autor(senha, autor_atual, cursor)
        senha_hash_original = obter_senha_hash_original_autor(autor_atual, cursor)
        return senha_hash_fornecida == senha_hash_original
    else:
        return valor_modificado == autor_atual.get(campo_bd)


def verificar_igualdade_dados_admin(campo_bd, valor_modificado, administrador, cursor):

    if campo_bd == 'senha':

        senha = valor_modificado
        senha_hash_fornecida = verificar_senha_fornecida_pelo_admin(senha, administrador, cursor)
        senha_hash_original = obter_senha_hash_original_admin(administrador, cursor)
        return senha_hash_fornecida == senha_hash_original
    else:
        return valor_modificado == administrador.get(campo_bd)


def verificar_igualdade_dados_postagem(campo, valor_modificado, postagem):

    return valor_modificado == postagem.get(campo)
