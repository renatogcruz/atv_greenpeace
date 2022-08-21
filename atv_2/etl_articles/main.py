from flask import Flask, request, jsonify

import services.bigquery as update_bq
import services.newsapi as update_sheets
import email_service


app = Flask(__name__)


@app.route("/")
def index():

    return jsonify({'status': 'success', 'massage': 'etl project newspaper articles about greenpeace brazil'}), 200


@app.route("/get_articles")
def get_articles():
    '''
    This endpoint does:
        1 - get data from News API
        2 - clean and make extra columns available
        3 - save data in sheets
    Programmed to run at 6:00
    Note: in case of failures, a warning will be sent to the email configured in email_service.py
    '''
    try:
        update_sheets.run()
        return jsonify({'status': 'success'}), 200

    except Exception:
        print('Oops! Something wrong. Send email')
        email_service.send_mail('ETL_ARTICLES - get_articles')
        return jsonify({'status': 'error'}), 500


@app.route("/update_bigquery")
def update_bigquery():
    '''
    This endpoint does:
        1 - read the sheets
        2 - save new and populated data in bigquery
    Programmed to run at 20:00
    Note: in case of failures, a warning will be sent to the email configured in email_service.py
    '''

    try:
        update_bq.run()
        return jsonify({'status': 'success'}), 200

    except Exception:
        print('Oops! Something wrong. Send email')
        email_service.send_mail('ETL_ARTICLES - update_bigquery')
        return jsonify({'status': 'error'}), 500


if __name__ == "__main__":  # On running python app.py
    app.run(debug=True)
