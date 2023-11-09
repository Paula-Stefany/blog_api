# blog_api

API de Blog
Esta é uma API de blog desenvolvida em Flask, com funcionalidades abrangentes para gerenciar autores, postagens e
administradores. A API oferece endpoints para realizar operações CRUD (Criar, Ler, Atualizar, Excluir) em diferentes 
entidades.

Endpoints Principais
Autorização
Para acessar determinados endpoints, é necessário incluir um token válido no cabeçalho da solicitação. Certifique-se de
obter um token através das rotas apropriadas.

Autores

Obter Todos os Autores:
Endpoint: /autores
Método: GET
Descrição: Retorna informações básicas de todos os autores cadastrados.

Obter um Autor Específico:
Endpoint: /autores/<nome_autor>
Método: GET
Descrição: Retorna informações básicas sobre autor cujo nome foi especificado no endpoint.

Novo Autor (Acesso com o token):
Endpoint: /autores
Método: POST
Descrição: Permite a um administrador enviar um convite de email de cadastro para um novo autor.

Editar Autor (Acesso com o token):
Endpoint: /autores/<nome_autor>
Método: PUT
Descrição: Permite a um autor editar suas próprias informações.

Excluir Autor (Acesso com o token):
Endpoint: /autores/<nome_autor>
Método: DELETE
Descrição: Permite a um autor excluir sua conta, incluindo todas as postagens associadas.

Postagens

Obter Todas as Postagens:
Endpoint: /postagens
Método: GET
Descrição: Retorna todas as postagens disponíveis.

Obter Postagem por Título:
Endpoint: /postagem/titulo/<titulo_postagem>
Método: GET
Descrição: Retorna informações sobre uma postagem específica com base no título.

Obter Postagens pelo nome do Autor:
Endpoint: /postagem/autor/<nome_autor>
Método: GET
Descrição: Retorna todas as postagens do autor cujo nome foi escrito  no endpoint.

Nova Postagem (Acesso com o token):
Endpoint: /postagem
Método: POST
Descrição: Permite a um autor criar uma nova postagem.

Editar Postagem (Acesso com o token):
Endpoint: /postagem/<titulo_postagem>
Método: PUT
Descrição: Permite a um autor editar suas próprias postagens.

Excluir Postagem (Acesso com o token):
Endpoint: /postagem/<titulo_postagem>
Método: DELETE
Descrição: Permite a um autor excluir suas próprias postagens.

Administradores

Visualizar Todos os Administradores (Acesso com o token):
Endpoint: /admins
Método: GET
Descrição: Retorna informações básicas de todos os administradores cadastrados.

Visualizar Dados de um Administrador (Acesso com o token):
Endpoint: /admin/<nome_admin>
Método: GET
Descrição: Retorna informações detalhadas sobre um administrador específico.

Histórico de Autor (Acesso com o token):
Endpoint: /historico_autor/<nome_autor>
Método: GET
Descrição: Retorna o histórico de um autor específico, disponível apenas para administradores.

Adicionar Novo Administrador (Acesso com o token):
Endpoint: /admin
Método: POST
Descrição: Permite a o administrador especial adicionar novos administradores enviando emails de cadastro.

Editar Dados do Administrador (Acesso com o token):
Endpoint: /admin/<nome_admin>
Método: PUT
Descrição: Permite a um administrador editar seus próprios dados.

Excluir Administrador (Acesso com o token):
Endpoint: /admin/<nome_admin>
Método: DELETE
Descrição: Permite a o administrador especial excluir a conta de outro administrador.

Excluir Autor(Acesso com o token)
Endpoint: /admin/excluir_autor/<id_autor>
Método: DELETE
Descrição: Permite a um administrador excluir os dados de um autor.

Excluir Postagem(Acesso com o token)
Endpoint: /admin/excluir_postagem/<id_postagem>
Método: DELETE
Descrição: Permite a um administrador excluir a postagem de um autor.

Configuração
Certifique-se de intalar todas as dependências presentes no arquivo requirements.txt, também foi usado o Mysql
workbench para criar o banco de dados blog e as tabelas autores, postagens e administradores. Acesse o arquivo
create_database_sql para conferir os comandos de criação do banco de dados e das tabelas.

Contribuição
Contribuições são bem-vindas! Se você encontrar problemas ou tiver sugestões para melhorar a API, sinta-se à vontade 
para abrir uma issue ou enviar um pull request.
