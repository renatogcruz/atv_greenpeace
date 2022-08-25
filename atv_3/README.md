### Exercício 3

Descrição de sintaxe SQL utilizado para esses diferentes cenários:

1. Cada analista da equipe de Inteligência de Dados tem um perfil próprio e temos uma conta genérica para conseguir lidar com bases de dados coletivas. No cenário em que o usuário `gp_user` gostaria de ter acesso para a tabela `press_data`, qual seria o código para disponibilizá-la?

`GRANT SELECT ON db_name.press_data TO 'gp_user'@'localhost' IDENTIFIED BY 'gp_user123';`

2. Em algumas vezes, mesmo após dar permissão uma vez, a tabela é reescrita com o parâmetro `drop` e perde as permissões. Qual o código que deve ser feito para que a tabela sempre herde os privilégios de forma padrão?

`ALTER DEFAULT PRIVILEGES in schema sales GRANT INSERT ON tables to group user_admin;`

3. Em um cenário que alguém não é mais responsável por uma tabela específica, qual o código para mudar a pessoa proprietária dessa tabela?

`REVOKE USAGE ON table table_name from group user;`

________________
#### Veja respostas detalhadas **[AQUI](https://github.com/renatogcruz/atv_greenpeace/blob/main/atv_3/atv_3.ipynb)**


_______________
# Observação:

A maior dificuldade desta atividade, para mim, foi a falta de familiaridade com gerenciamento de bancos de dados (autorizações de acesso). Apesar de trabalhar com bancos de dados diariamente, sempre recebo acesso aos bancos que preciso alimentar. Então, minha experiência é sempre na infraestrutura e engenharia de dados, e não no gerenciamento dos bancos. 

Para responder as perguntas li os tutoriais da AWS e pesquisei sites como stackoverflow entre outros. Uma dificuldade extra foi a falta de aplicação num exemplo real, o que não permitiu a correção de possíveis erros das sintaxes respondidas. 
