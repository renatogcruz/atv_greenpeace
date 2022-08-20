# ETL CLIPPING | GREENPEACE



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