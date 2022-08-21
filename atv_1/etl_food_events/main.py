from flask import Flask, jsonify, url_for, redirect
import pandas as pd

from os import environ
from dotenv import load_dotenv

import services.bigquery as bq
from google.cloud import bigquery

from gcp import get_credentials

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'biguery_credential.json'


app = Flask(__name__)


@app.route("/")
def index():

    return jsonify({'status': 'success', 'massage': 'etl project food events - Greenpeace Brazil'}), 200


@app.route("/access_bq")
def access_bq():
    # simple non parameterized query
    client = bigquery.Client()
    # table_id = "greenpeace-360016.db_food.food_events"

    query = """
        SELECT * 
        FROM `bigquery-public-data.fda_food.food_events`;
        """

    query_res = client.query(query)
    # query_res.result()  # Wait for the job to complete.

    query_df = query_res.to_dataframe()
    # query_df.to_csv("food_events.csv")
    # print(f'type: {type(query_res)}')
    # to print in the console
    # for row in query_res:
    #     print(row)

    return redirect(url_for('read_bq', query_df=query_df))


@app.route("/save_bq", methods=["GET"])
def save_bq(query_df):

    query_df = query_df

    # Connect to bigquery
    project_id = environ['PROJECT_ID']
    credentials = get_credentials()

    query_df.to_gbq(destination_table='fda_food.food_events', project_id=project_id,
                    credentials=credentials, if_exists='replace')

    return jsonify({'status': 'success', 'massage': f'total number of observations = {df.shape[0]}'}), 200


@app.route("/read_bq", methods=["GET"])
def read_bq(query_df):

    query_df = query_df

    # Connect to bigquery
    project_id = environ['PROJECT_ID']
    credentials = get_credentials()

    query = f'''
    SELECT *
    FROM fda_food.food_events
    '''

    df = pd.read_gbq(
        query, credentials=credentials,  project_id=project_id)

    return jsonify({'status': 'success', 'massage': {df.to_dict("records")}}), 200


if __name__ == "__main__":  # On running python app.py
    app.run(debug=True)
