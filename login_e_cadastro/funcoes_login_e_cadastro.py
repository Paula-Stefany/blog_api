from funcoes_senha_hash import gerar_senha_hash


def inserir_novo_autor(nome, email, biografia, salt, senha_hash, cursor, conexao):

    comando = 'insert into autores(nome, email, biografia, salt, senha_hash) values(%s, %s, %s, %s, %s)'
    cursor.execute(comando, (nome, email, biografia, salt, senha_hash))
    conexao.commit()


def inserir_novo_admin(nome, email, salt, senha_hash, cursor, conexao):

    comando_insercao = 'insert into administradores(nome, email, salt, senha_hash) values(%s, %s, %s, %s)'
    cursor.execute(comando_insercao, (nome, email, salt, senha_hash))
    conexao.commit()


def conferir_acesso_autor(email, senha, cursor):

    comando = 'SELECT id_autor, salt, senha_hash FROM autores WHERE email = %s;'
    cursor.execute(comando, (email,))
    autor = cursor.fetchone()
    if not autor:
        return None

    salt = autor['salt'].encode('utf-8')
    hash_verdadeira = autor['senha_hash']
    hash_dado = gerar_senha_hash(senha, salt).decode('utf-8')
    if hash_verdadeira == hash_dado:
        return autor

    return None


def conferir_acesso_administrador(email, senha, cursor):

    comando = 'select id_admin, salt, senha_hash from administradores where email = %s;'
    cursor.execute(comando, (email,))
    administrador = cursor.fetchone()
    if not administrador:
        return None

    hash_verdadeira = administrador['senha_hash']
    salt = administrador['salt'].encode('utf-8')
    hash_dado = gerar_senha_hash(senha, salt).decode('utf-8')

    if hash_verdadeira == hash_dado:
        return administrador

    return None


def conferir_dados_login(email, senha, cursor):

    autor = conferir_acesso_autor(email, senha, cursor)
    if autor:
        id_autor = autor['id_autor']
        tipo_usuario = 'autor'
        return id_autor, tipo_usuario

    administrador = conferir_acesso_administrador(email, senha, cursor)
    if administrador is not None:
        id_administrador = administrador['id_admin']
        tipo_usuario = 'administrador'
        return id_administrador, tipo_usuario

    else:
        return None, None


def verificar_se_email_admin_ja_existe_no_banco(email, cursor):

    comando = 'select * from administradores where email = %s'
    cursor.execute(comando, (email,))
    email = cursor.fetchone()
    return email


def verificar_se_email_autor_ja_existe_no_banco(email, cursor):

    comando = 'select * from autores where email = %s'
    cursor.execute(comando, (email,))
    email = cursor.fetchone()
    return email
