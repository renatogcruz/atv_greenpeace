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


