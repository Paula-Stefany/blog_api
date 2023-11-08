import bcrypt


def gerar_salt():

    salt = bcrypt.gensalt()
    return salt


def gerar_senha_hash(senha, salt):

    hash_gerada = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_gerada


def obter_senha_hash_original_autor(autor_atual, cursor):

    id_autor = autor_atual.get('id_autor')
    comando = 'select senha_hash from autores where id_autor = %s'
    cursor.execute(comando, (id_autor,))
    autor = cursor.fetchone()
    senha_hash = autor['senha_hash']

    return senha_hash


def pegar_salt_original_do_autor(autor_atual, cursor):

    id_autor = autor_atual['id_autor']
    comando = 'select salt from autores where id_autor = %s'
    cursor.execute(comando, (id_autor,))
    autor = cursor.fetchone()
    salt = autor['salt']
    return salt.encode('utf-8')


def verificar_senha_fornecida_pelo_autor(senha, autor_atual, cursor):

    salt = pegar_salt_original_do_autor(autor_atual, cursor)
    senha_hash_formada = gerar_senha_hash(senha, salt)
    return senha_hash_formada.decode('utf-8')


def obter_senha_hash_original_admin(admin_atual, cursor):

    id_admin = admin_atual.get('id_admin')
    comando = 'select senha_hash from administradores where id_admin = %s'
    cursor.execute(comando, (id_admin,))
    autor = cursor.fetchone()
    senha_hash = autor['senha_hash']

    return senha_hash


def pegar_salt_original_do_admin(administrador, cursor):

    id_admin = administrador['id_admin']
    comando = 'select salt from administradores where id_admin = %s'
    cursor.execute(comando, (id_admin,))
    admin = cursor.fetchone()
    salt = admin['salt']
    return salt.encode('utf-8')


def verificar_senha_fornecida_pelo_admin(senha, administrador, cursor):

    salt = pegar_salt_original_do_admin(administrador, cursor)
    senha_hash_formada = gerar_senha_hash(senha, salt)
    return senha_hash_formada.decode('utf-8')
