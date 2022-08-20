from flask import Flask, request, jsonify
import pandas as pd

from os import environ
from dotenv import load_dotenv

import services.bigquery as bq


app = Flask(__name__)


@app.route("/")
def index():

    return jsonify({'status': 'success', 'massage': 'etl project food events - Greenpeace Brazil'}), 200


@app.route("/access_bq")
def access_bq():
    df = bq.dataframe()
    print(df.head())

    return jsonify({'status': 'success', 'massage': 'etl project food events - Greenpeace Brazil'}), 200


if __name__ == "__main__":  # On running python app.py
    app.run(debug=True)
