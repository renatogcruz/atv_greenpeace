import mysql
import email_service
from flask import Flask, request, jsonify
import pandas as pd
import pickle
import numpy as np

from os import environ
from dotenv import load_dotenv

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


@app.route("/create_task/<site>/<category>/<crawler_date>")
def create_task(site, category, crawler_date):

    query = f"""
    SELECT id, site, url, category, crawler_date
    FROM products 
    WHERE processed_at IS NULL AND site = '{site}' AND crawler_date = '{crawler_date}' AND category = '{category}';
    """

    dataframe = pd.read_sql_query(query, mysql.conn())
    for index, row in dataframe.iterrows():
        try:
            task_name = f"{row['site']}_{row['id']}_p"
            info = dict(request_url=f"{environ['CLOUD_RUN_GCP']}/{site}/detail",
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
    variable = response['']
    try:
        # convert integers to float
        float_features = [float(x) for x in request.form.values()]
        # convert floats to array
        features = [np.array(float_features)]

        prediction = model.predict(features)

        # to save mySQL
        # dataframe = functions.format_data_types(dataframe)
        # dataframe.to_sql(environ['TABLE_DETAILS_PRODUCTION'], mysql.conn(),
        #                  if_exists='append', index=False)
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        processed_at = {
            'processed_at': time
        }
        response = mysql.update_product(
            processed_at, int(id), environ['TABLE_PRODUCT_PRODUCTION'])

        return 'render_template("index.html", prediction_text=f"The flower species is {prediction}")'

    except Exception:
        # to save LOGS
        print('Oops! Something wrong. Send email')
        email_service.send_mail(f'Predict {variable}')

        return jsonify({'message': f'id = {id} | failed attempt'}), 500


if __name__ == "__main__":  # On running python app.py
    app.run(debug=True)
