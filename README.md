# blog_api
 projeto back-end api blog
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
Descrição: Retorna informações detalhadas sobre um autor específico.
Novo Autor (Acesso Restrito):

Endpoint: /autores
Método: POST
Descrição: Permite a um administrador enviar convites para novos autores.
Editar Autor (Perfil de Autor):

Endpoint: /autores/<nome_autor>
Método: PUT
Descrição: Permite a um autor editar suas próprias informações.
Excluir Autor (Perfil de Autor):

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
Obter Postagens de um Autor:

Endpoint: /postagem/autor/<nome_autor>
Método: GET
Descrição: Retorna todas as postagens de um autor específico.
Nova Postagem (Perfil de Autor):

Endpoint: /postagem
Método: POST
Descrição: Permite a um autor criar uma nova postagem.
Editar Postagem (Perfil de Autor):

Endpoint: /postagem/<titulo_postagem>
Método: PUT
Descrição: Permite a um autor editar suas próprias postagens.
Excluir Postagem (Perfil de Autor):

Endpoint: /postagem/<titulo_postagem>
Método: DELETE
Descrição: Permite a um autor excluir suas próprias postagens.
Administradores
Visualizar Todos os Administradores (Acesso Restrito):

Endpoint: /admins
Método: GET
Descrição: Retorna informações básicas de todos os administradores cadastrados.
Visualizar Dados de um Administrador (Acesso Restrito):

Endpoint: /admin/<nome_admin>
Método: GET
Descrição: Retorna informações detalhadas sobre um administrador específico.
Histórico de Autor (Acesso Restrito):

Endpoint: /historico_autor/<nome_autor>
Método: GET
Descrição: Retorna o histórico de um autor específico, disponível apenas para administradores.
Adicionar Novo Administrador (Acesso Restrito):

Endpoint: /admin
Método: POST
Descrição: Permite a um administrador adicionar novos administradores enviando convites por e-mail.
Editar Dados do Administrador (Acesso Restrito):

Endpoint: /admin/<nome_admin>
Método: PUT
Descrição: Permite a um administrador editar informações de outros administradores.
Excluir Administrador (Acesso Restrito):

Endpoint: /admin/<nome_admin>
Método: DELETE
Descrição: Permite a um administrador excluir a conta de outro administrador.
Configuração
Certifique-se de seguir as instruções de instalação e execução no seu ambiente local. Além disso, atente-se aos 
requisitos específicos mencionados, como a necessidade de um banco de dados MySQL.

Contribuição
Contribuições são bem-vindas! Se você encontrar problemas ou tiver sugestões para melhorar a API, sinta-se à vontade 
para abrir uma issue ou enviar um pull request.
