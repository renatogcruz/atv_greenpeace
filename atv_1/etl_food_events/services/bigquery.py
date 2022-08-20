from os import environ
from dotenv import load_dotenv
import pandas as pd
from google.cloud import bigquery

load_dotenv()


def dataframe():

    # Start the BigQuery Client
    client = bigquery.Client(environ["GOOGLE_APPLICATION_CREDENTIALS"])
    # Input your Query Syntax here; You may try it first at https://console.cloud.google.com/bigquery
    QUERY = ('SELECT * FROM `bigquery-public-data.fda_food.food_events`;')
    query_job = client.query(QUERY)    # Start Query API Request
    query_result = query_job.result()  # Get Query Result
    df = query_result.to_dataframe()   # Save the Query Resultto Dataframe
    # ---------------------------------------------
    # ---- Continue Data Analysis with your DF ----
    # ---------------------------------------------

    return df
