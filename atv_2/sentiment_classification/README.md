# ETL CLIPPING | GREENPEACE

## Estrutura do banco MySQL


CREATE TABLE `articles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `urlToImage` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `publishedAt` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  `processed_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41081 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `sentiment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_id` int NOT NULL,
  `sentiment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `sentiment_FK` (`article_id`),
  CONSTRAINT `sentiment_FK` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37516 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;





## Deploy to GCP



___________

`gcloud config get-value project` 

___________


`gcloud auth login`

`gcloud config set project PROJECT-NAME`

`gcloud builds submit --tag gcr.io/PROJECT-NAME/RUN-NAME`

`gcloud beta run deploy RUN-NAME --image gcr.io/PROJECT-NAME/RUN-NAME --region us-central1 --platform managed`



___________



## WARNING:

Don't forget to install the library **Gunicorn**

*[Gunicorn](https://pypi.org/project/gunicorn/) Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX*