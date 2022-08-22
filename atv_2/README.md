### Exercício 2

A tarefa aqui foi usar a [News API](https://newsapi.org/) para fazer uma extração diária das 100 matérias mais recentes sobre o `Greenpeace Brasil`. Em seguida, montar um fluxo em que a equipe de imprensa possa preencher manualmente se a matéria é positiva, negativa ou neutra. Depois, após o preenchimento, essa tabela quando preenchida (e se preenchida) deve ser enviada para o BigQuery ou Google Sheets. 

Essa tarefa foi realizada em duas condições:

______________
### A primeira no [documento do tipo ipynb](https://github.com/renatogcruz/atv_greenpeace/blob/main/atv_2/atv_2.ipynb) (jupyter notebook ou google colab) 

Nesta condição, o trabalho foi realizado seguindo estes passos:

1. Importar os dados da News API sobre o Greenpeace Brasil

Requisições de API (requests) via método `GET` (HTTP method) no formato `JSON`

2. Limpeza e disponibilização

Organização dos dados nas colunas e adicção de campo para classificação manual da equipe de imprensa com a avaliação de sentimento

Apos essa etapa, as informações coletadas foram exportadas para a tabela `articles` do Google Sheets para que a equipe de imprensa possa fazer sua avaliação de sentimento.

A tabela `articles` do Google Sheets pode ser visualizada [aqui](https://docs.google.com/spreadsheets/d/1-UeC6co2I1DSfTmQACf7euOJRKHsRX_jUagSmdavCZo/edit)


______________
### A segunda em 2 projetos de integração como forma de propor a automatização dessa ativada.

A primeira integração foi realizada seguindo os passos propostos pelo enunciado: importação dos dados, limpeza e disponibilização dos dados, adição de coluna para **classificação manual** de sentimento e exportação dos dados.

Para isso foi usado o framework flask e o trabalho se estrutura em endpoints. Para uma explicação mais detalhada, [acesse](https://github.com/renatogcruz/atv_greenpeace/tree/main/atv_2/etl_articles).


A segunda integração também foi realizada seguindo os passos propostos pelo enunciado mas seguindo uma lógica de maior autônomia do código: importação dos dados, limpeza e disponibilização dos dados, adição de coluna para **classificação automática** de sentimento e exportação dos dados.

Para isso foi usado o framework flask e o trabalho se estrutura em endpoints. Para uma explicação mais detalhada, [acesse](https://github.com/renatogcruz/atv_greenpeace/tree/main/atv_2/sentiment_classification).


______________

# Observações:

A API `News API`, em sua versão `Developer` (*totally free*), apresenta limitações que impediu a realização da coleta das últimas 100 notícias recentes sobre o `Greenpeace Brasil`.

A primeira limitação é o número de requisições diária, `100 requests`. 

Para endpoint `Everything` existe a limitação de buscar apenas os `dia corrente` e seu `dia interior`. 

Isso dificultou a busca das últimas 100 públicações distintas. Esse endpoint, na versão *totally free* não permite que se adicione valores de datas além do dia anterior do dia corrente.

A segunda estrátegia adotada foi `iterar` esse endpoint `passando datas subsequentes`, do `dia corrente para trás`. O problema aqui é que mesmo os dias em que `não há públicações` sobre o Greenpeace, a `contagem de requisição feita`. Somando isso as `públicações repetidas` (as mesma públicação pode estar visível em dias diferentes), as requisições realizadas durante a construção da atividade, os testes, o número final de requisições diárias ficou comprometida.




