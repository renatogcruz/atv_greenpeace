# ETL CLIPPING | GREENPEACE

## Install the dependencies

```
cachetools==5.2.0
certifi==2022.6.15
charset-normalizer==2.1.1
click==8.1.3
colorama==0.4.5
db-dtypes==1.0.3
Flask==2.2.2
google-api-core==2.8.2
google-auth==2.11.0
google-auth-oauthlib==0.5.2
google-cloud==0.34.0
google-cloud-bigquery==3.3.2
google-cloud-bigquery-storage==2.14.2
google-cloud-core==2.3.2
google-crc32c==1.3.0
google-resumable-media==2.3.3
googleapis-common-protos==1.56.4
grpcio==1.47.0
grpcio-status==1.47.0
gunicorn==20.1.0
idna==3.3
importlib-metadata==4.12.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
numpy==1.21.6
oauthlib==3.2.0
packaging==21.3
pandas==1.1.5
pandas-gbq==0.17.8
proto-plus==1.22.0
protobuf==4.21.5
pyarrow==9.0.0
pyasn1==0.4.8
pyasn1-modules==0.2.8
pydata-google-auth==1.4.0
pyparsing==3.0.9
python-dateutil==2.8.2
python-dotenv==0.20.0
pytz==2022.2.1
requests==2.28.1
requests-oauthlib==1.3.1
rsa==4.9
six==1.16.0
typing_extensions==4.3.0
urllib3==1.26.11
Werkzeug==2.2.2
zipp==3.8.1
```

Run command `pip install -r requirements.txt`

Python version `3.7.0`


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