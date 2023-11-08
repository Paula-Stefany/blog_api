from funcoes_verificacao_igualdade import (verificar_igualdade_dados_autor, verificar_igualdade_dados_postagem,
                                           verificar_igualdade_dados_admin)
from funcoes_senha_hash import gerar_salt, gerar_senha_hash


def adicionar_comandos_sql_autores(partes_sql, valores, modificacoes, autor_atual, cursor):

    lista_campos = ['nome', 'email', 'biografia', 'senha']

    for campo, valor in modificacoes.items():
        if campo in lista_campos:
            valor_modificado = modificacoes[campo]

            if not verificar_igualdade_dados_autor(campo, valor_modificado, autor_atual, cursor):
                if campo == 'senha':
                    campo = 'senha_hash'
                    salt = gerar_salt()
                    senha_hash = gerar_senha_hash(valor_modificado, salt)
                    valor_modificado = senha_hash

                    partes_sql.append('salt = %s')
                    valores.append(salt)

                partes_sql.append(f'{campo} = %s')
                valores.append(valor_modificado)


def adicionar_comandos_sql_postagem(partes_sql, valores, modificacoes, postagem):

    lista_campos = ['titulo', 'assunto']

    for campo in lista_campos:
        if campo in modificacoes:
            valor_modificado = modificacoes[campo]
            if not verificar_igualdade_dados_postagem(campo, valor_modificado, postagem):
                partes_sql.append(f'{campo} = %s')
                valores.append(valor_modificado)


def adicionar_comandos_sql_admins(partes_sql, valores, modificacoes, administrador, cursor):

    lista_campos = ['nome', 'email', 'senha']

    for campo, valor in modificacoes.items():
        if campo in lista_campos:
            valor_modificado = modificacoes[campo]

            if not verificar_igualdade_dados_admin(campo, valor_modificado, administrador, cursor):
                if campo == 'senha':
                    campo = 'senha_hash'
                    salt = gerar_salt()
                    senha_hash = gerar_senha_hash(valor_modificado, salt)
                    valor_modificado = senha_hash

                    partes_sql.append('salt = %s')
                    valores.append(salt)

                partes_sql.append(f'{campo} = %s')
                valores.append(valor_modificado)
