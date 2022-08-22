import pandas as pd
import requests
import json

import services.functions as functions
import services.gsheets as gsheets

from os import environ
from dotenv import load_dotenv

import mysql

load_dotenv()


def get_all_articles(keyword='Greenpeace Brasil'):

    response = requests.get(
        f"{environ['URL_API']}/everything?q={keyword}&apiKey={environ['KEY_API']}")
    try:
        r = response.json()
        return r
    except requests.exceptions.RequestException as e:
        return SystemExit(e)


def run():

    r = get_all_articles()
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

    return dict(status='success', message='Saved article in Google Sheets')
