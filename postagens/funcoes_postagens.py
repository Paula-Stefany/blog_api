def obter_postagens(cursor):

    comando = ('select a.nome, p.titulo, p.assunto from autores as a inner join postagens as p on '
               'a.id_autor = p.id_autor order by titulo;')
    cursor.execute(comando)
    postagens = cursor.fetchall()
    return postagens


def obter_postagem_pelo_autor(nome_autor, cursor):

    comando = ('select a.nome, p.titulo, p.assunto from autores as a inner join postagens as p on a.id_autor = '
               'p.id_autor where a.nome = %s')
    cursor.execute(comando, (nome_autor,))
    postagens = cursor.fetchall()
    return postagens


def obter_postagem_pelo_titulo(titulo_postagem, cursor):

    comando = ('select a.nome, p.titulo, p.assunto from autores as a inner join postagens as p'
               ' on a.id_autor = p.id_autor where titulo = %s')
    cursor.execute(comando, (titulo_postagem,))
    postagens = cursor.fetchall()
    return postagens


def obter_postagem_pelo_id_postagem(id_postagem, cursor):

    comando = 'select * from postagens where id_postagem = %s'
    cursor.execute(comando, (id_postagem,))
    postagem = cursor.fetchone()
    return postagem


def inserir_nova_postagem(id_autor, titulo, assunto, cursor, conexao):

    try:
        comando = 'insert into postagens (id_autor, titulo, assunto) values(%s, %s, %s);'
        cursor.execute(comando, (id_autor, titulo, assunto))
        conexao.commit()

    except Exception as erro:
        conexao.rollback()
        raise erro


def obter_postagem_completa_do_autor(id_autor, titulo, cursor):

    comando = ('select * from postagens as p inner join autores as a on a.id_autor = p.id_autor where p.titulo = %s and'
               ' p.id_autor = %s ')
    cursor.execute(comando, (titulo, id_autor))
    postagem = cursor.fetchone()
    return postagem


def deletar_postagem_pelo_titulo(id_autor, titulo_postagem, cursor, conexao):

    try:
        comando = 'delete from postagens where id_autor = %s and titulo = %s;'
        cursor.execute(comando, (id_autor, titulo_postagem))
        conexao.commit()

    except Exception as erro:
        raise erro


def deletar_postagem_pelo_id_postagem(id_postagem, cursor, conexao):

    try:
        comando = 'delete from postagens where id_postagem = %s'
        cursor.execute(comando, (id_postagem,))
        conexao.commit()

    except Exception as erro:
        raise erro


def deletar_todas_postagens_de_um_autor(id_autor, cursor, conexao):

    try:
        comando = 'delete from postagens where id_autor = %s'
        cursor.execute(comando, (id_autor,))
        conexao.commit()

    except Exception as erro:
        raise erro


def verficar_possivel_titulo_duplicado(id_autor, titulo, cursor):

    comando = 'select * from postagens where id_autor = %s and titulo = %s'
    cursor.execute(comando, (id_autor, titulo))
    postagem = cursor .fetchone()
    if not postagem:
        return False
    return True
