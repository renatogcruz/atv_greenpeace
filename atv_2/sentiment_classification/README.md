# SENTIMENT CLASSIFICATION | GREENPEACE

## Endpoints

Essa integração se resume em 4 endpoints:

1. **index** `https://url_cloud_run_gcp/`

Esse endpoint é de boas-vindas ao projeto e é útil apenas para o ambiente de teste. Não tem função na infraestrutura da Cloud Computing.

2. **get_articles** `https://url_cloud_run_gcp/get_articles`

Este endpoint faz: 
1 - requisições de dados da News API; 
2 - limpeza e disponibilização de campo para classificação manual da equipe de imprensa com a avaliação de sentimento; 
3 - salvar apenas dados novos na tabela `TABLE_ARTICLES` do `MySQL` (´banco de coleta´).

A proposta de execução deste endpoint no cloud scheduler é às 6:00, horário posterior as atualizações das notícias matinais dos jornais.

Como forma de autônomia da integração, este endpoint contém um serviço de aviso via email em caso de apresentar falhas.

3. **create_task/<description>** `https://url_cloud_run_gcp/create_task/<description>`

Este endpoint faz:
1 - itera a tabela `TABLE_ARTICLES` do `MySQL` (apenas `processed_at IS NULL`, ou seja, aapenas notícias que não contenham a coluna `sentiment` preenchido);
2 - cria uma Google Task
3 - faz uma requisição `POST` para o endpoint seguinte.

4. **predict** `https://url_cloud_run_gcp/predict`

Este endpoint é iniciado automaticamente pelo Google Task e faz:
1 - requece um payload (ID e DESCRIPTION da tabela `TABLE_ARTICLES` do `MySQL`);
2 - executa a predição no modelo previamente treinado para classificação de sentimento.
3 - salva resutlado na tabela `TABLE_PREDICT` do ´MySQL´ (´banco de sentimento´).


## Install the dependencies

```
cachetools==5.2.0
certifi==2022.6.15
charset-normalizer==2.1.1
click==8.1.3
colorama==0.4.5
filelock==3.8.0
Flask==2.2.2
google-auth==2.11.0
google-cloud==0.34.0
google-play-scraper==1.2.2
gunicorn==20.1.0
huggingface-hub==0.8.1
idna==3.3
importlib-metadata==4.12.0
itsdangerous==2.1.2
Jinja2==3.1.2
joblib==1.1.0
MarkupSafe==2.1.1
numpy==1.21.6
packaging==21.3
pandas==1.1.5
pickle5==0.0.12
pyasn1==0.4.8
pyasn1-modules==0.2.8
PyMySQL==1.0.2
pyparsing==3.0.9
python-dateutil==2.8.2
python-dotenv==0.20.0
python-http-client==3.3.7
pytz==2022.2.1
PyYAML==6.0
regex==2022.8.17
requests==2.28.1
rsa==4.9
scikit-learn==1.0.2
scipy==1.7.3
sendgrid==6.9.7
six==1.16.0
sklearn==0.0
starkbank-ecdsa==2.0.3
threadpoolctl==3.1.0
tokenizers==0.12.1
torch==1.12.1
tqdm==4.64.0
transformers==4.21.1
typing_extensions==4.3.0
urllib3==1.26.11
Werkzeug==2.2.2
zipp==3.8.1
```

Run command `pip install -r requirements.txt`

Python version `3.7.0`

## MySQL database structure

```
CREATE TABLE articles (
  id int NOT NULL AUTO_INCREMENT,
  author text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  title text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  description text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  url text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  urlToImage text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  publishedAt text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  content text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  name text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  processed_at timestamp NULL DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=41081 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```
CREATE TABLE sentiment (
  id int NOT NULL AUTO_INCREMENT,
  article_id int NOT NULL,
  sentiment text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY sentiment_FK (article_id),
  CONSTRAINT `sentiment_FK` FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37516 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## Deploy to GCP

___________

See what the current project is:

`gcloud config get-value project` 

___________

login:

`gcloud auth login`

Config:

`gcloud config set project PROJECT-NAME`

Builds:

`gcloud builds submit --tag gcr.io/PROJECT-NAME/RUN-NAME`

Deploy:

`gcloud beta run deploy RUN-NAME --image gcr.io/PROJECT-NAME/RUN-NAME --region us-central1 --platform managed`



___________



## WARNING:

Don't forget to install the library **Gunicorn**

*[Gunicorn](https://pypi.org/project/gunicorn/) Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX*
