from os import environ
from google.oauth2 import service_account
import pandas as pd
from gcp import get_credentials

from gsheets import read_gsheets


# função para ler todos as linhas do sheets que tenham a coluna 'sentiment' preenchido
def read_google_sheets_and_return_rows_with_filled_sentiment_column():

    dataframe = read_gsheets(environ['GOOGLE_SHEETS_ID'], 0)
    dataframe = dataframe[dataframe['sentiment'] != '']

    return dataframe


def run():
    project_id = 'NAME_PROJECT'
    credentials = get_credentials()

    articles = read_google_sheets_and_return_rows_with_filled_sentiment_column()

    # read BIGQUERY
    query = '''
    SELECT * 
    FROM tb_articles_sentiments    
    '''
    bq_df = pd.read_gbq(
        query, credentials=credentials,  project_id=project_id)

    articles_news = pd.merge(articles, bq_df, indicator=True, how='outer').query(
        '_merge=="left_only"').drop('_merge', axis=1)

    # SAVING RAW day sale data in bigquery
    articles_news.to_gbq(destination_table='articles.tb_articles_sentiments', project_id=project_id,
                         credentials=credentials, if_exists='append')

    return dict(status='success', message='saved article sentiment rating')
