import mysql
import email_service
from flask import Flask, request, jsonify
import pandas as pd
import pickle
import numpy as np
import requests

from os import environ
from dotenv import load_dotenv

import services.newsapi as newapi
import services.tasks as tasks

from pytz import timezone
from datetime import datetime, timedelta
tz = timezone('America/Sao_Paulo')


app = Flask(__name__)

# load de pickle model
# rb is the argument to read the file
model = pickle.load(open("model.pkl", "rb"))


@app.route("/")
def teste():

    return "Hello, Greenpeace"


@app.route("/get_articles")
def get_articles():
    '''
    This endpoint does:
        1 - get data from News API
        2 - clean and make extra columns available
        3 - save data in table_articles MySQL
    Programmed to run at 6:00
    Note: in case of failures, a warning will be sent to the email configured in email_service.py
    '''
    try:
        r = newapi.get_all_articles()
        articles = pd.DataFrame(r['articles'])

        articles['name'] = articles['source'].apply(functions.get_name)
        articles = articles[['author', 'title', 'description',
                            'url', 'urlToImage', 'publishedAt', 'content', 'name']]
        articles = articles.sort_values(by=['publishedAt'], ascending=False)

        # ler SHEETS e ver qual salvar
        sheets_df = pd.read_sql_query(
            f"SELECT * FROM {environ['TABLE_ARTICLES']}", mysql.conn())
        sheets_df = sheets_df[['author', 'title', 'description',
                               'url', 'urlToImage', 'publishedAt', 'content', 'name']]
        articles_news = pd.merge(articles, sheets_df, indicator=True, how='outer').query(
            '_merge=="left_only"').drop('_merge', axis=1)

        # create sentiment column
        articles_news['sentiment'] = None
        articles_news = articles_news[['author', 'title', 'description', 'url',
                                       'urlToImage', 'publishedAt', 'content', 'name', 'sentiment']]

        articles_news.to_sql(environ['TABLE_ARTICLES'], mysql.conn(),
                             if_exists='append', index=False)

        # create TASK
        info_df = articles_news.iloc[0]
        description = info_df['description']

        url = f"{environ['CLOUD_RUN_GCP']}/create_task/{description}"
        response_task = requests.get(url)
        if response_task.status_code == 200:
            return jsonify(dict(status='success', message=response_task.text)), 200
        else:
            return jsonify(dict(status='error', message=response_task.text)), 401

    except Exception:
        print('Oops! Something wrong. Send email')
        email_service.send_mail('ETL_ARTICLES - get_articles')
        return jsonify({'status': 'error'}), 500


@app.route("/create_task/<description>")
def create_task(description):

    query = f"""
    SELECT id, description
    FROM TABLE_ARTICLES 
    WHERE processed_at IS NULL AND description = '{description}';
    """

    dataframe = pd.read_sql_query(query, mysql.conn())
    for index, row in dataframe.iterrows():
        try:
            task_name = f"{row['site']}_{row['id']}_p"
            info = dict(request_url=f"{environ['CLOUD_RUN_GCP']}/predict",
                        payload=row.to_dict())
            print(f'task_name: {task_name} | info: {info}')
            tasks.create_task(
                info, environ['QUEUE_NAME'], task_name)
        except Exception:
            continue

    print(f'create tasks {site} {category}: ok')

    return jsonify(dict(status='success')), 200


@app.route("/predict", methods=["POST"])
def predict():

    response = request.json
    variable = response['description']
    try:
        # convert integers to float
        float_features = [float(x) for x in request.form.values()]
        # convert floats to array
        features = [np.array(float_features)]

        prediction = model.predict(features)

        # to save mySQL
        dataframe.to_sql(environ['TABLE_PREDICT'], mysql.conn(),
                         if_exists='append', index=False)
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        processed_at = {
            'processed_at': time
        }
        response = mysql.update_product(
            processed_at, int(id), environ['TABLE_ARTICLES'])

        return jsonify({'status': 'success'}), 200

    except Exception:
        # to save LOGS
        print('Oops! Something wrong. Send email')
        email_service.send_mail(f'Predict {variable}')

        return jsonify({'message': f'id = {id} | failed attempt'}), 500


if __name__ == "__main__":  # On running python app.py
    app.run(debug=True)
