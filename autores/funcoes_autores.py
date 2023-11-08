def obter_dados_basicos_autores(cursor):

    comando = 'select nome, email, biografia from autores;'
    cursor.execute(comando)
    autores = cursor.fetchall()
    if not autores:
        return False
    return autores


def obter_dados_basicos_autor(nome_autor, cursor):

    comando = 'select nome, email, biografia from autores where nome = %s'
    cursor.execute(comando, (nome_autor,))
    autor = cursor.fetchone()
    if not autor:
        return False
    return autor


def obter_dados_completos_autor(id_autor, nome_autor, cursor):

    comando = 'select * from autores where id_autor = %s and nome = %s'
    cursor.execute(comando, (id_autor, nome_autor))
    autor = cursor.fetchone()
    if not autor:
        return False
    return autor


def deletar_autor(id_autor, nome_autor, cursor, conexao):

    comando_exclusao = 'delete from autores where id_autor = %s and nome = %s'
    cursor.execute(comando_exclusao, (id_autor, nome_autor))
    conexao.commit()


def verificar_existencia_do_autor(id_autor, cursor):

    comando = 'select * from autores where id_autor = %s'
    cursor.execute(comando, (id_autor,))
    autor = cursor.fetchone()
    return autor


def deletar_autor_pelo_id(id_autor, cursor, conexao):

    comando_exclusao = 'delete from autores where id_autor = %s'
    cursor.execute(comando_exclusao, (id_autor,))
    conexao.commit()
