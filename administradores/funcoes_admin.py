def obter_historico_autor(nome_autor, cursor):

    comando = ('select a.id_autor, p.id_postagem, a.nome, a.email, p.titulo, p.assunto from autores as a left join '  
               'postagens as p on a.id_autor = p.id_autor where a.nome = %s;')
    cursor.execute(comando, (nome_autor,))
    historico_autor = cursor.fetchall()
    return historico_autor


def verificar_admin_especial(id_admin, email_admin_especial, cursor):

    comando_verificacao = 'select email from administradores where id_admin = %s'
    cursor.execute(comando_verificacao, (id_admin,))
    admin = cursor.fetchone()
    if admin['email'] == email_admin_especial:
        return True
    return False


def obter_dados_basicos_admin(nome_admin, cursor):

    comando_get = 'select id_admin, nome, email from administradores where nome = %s'
    cursor.execute(comando_get, (nome_admin,))
    dados_admin = cursor.fetchone()
    return dados_admin


def obter_dados_administradores(cursor):

    comando_obter_administradores = 'select id_admin, nome, email from administradores;'
    cursor.execute(comando_obter_administradores)
    administradores = cursor.fetchall()
    return administradores


def obter_dados_admin_unico(nome_admin, cursor):

    comando = 'select nome, email, id_admin from administradores where nome = %s'
    cursor.execute(comando, (nome_admin,))
    administrador = cursor.fetchone()
    return administrador


def verificar_permicao_administrador(id_admin, nome_admin, cursor):

    comando = 'select * from administradores where id_admin = %s and nome = %s'
    cursor.execute(comando, (id_admin, nome_admin))
    administrador = cursor.fetchone()
    return administrador


def deletar_administrador(nome, cursor, conexao):

    comando = 'delete from administradores where nome = %s'
    cursor.execute(comando, (nome,))
    conexao.commit()
