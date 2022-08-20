from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():

    return jsonify({'status': 'success', 'massage': 'etl project newspaper articles about greenpeace brazil'}), 200


@app.route("/get_articles")
def get_articles():

    # Importação (dados API)
    # Limepza e disponibilização
    # salva no Google Sheets
    # Run -> as 6 horas

    return jsonify({'status': 'success', 'massage': 'etl project newspaper articles about greenpeace brazil'}), 200


@app.route("/update_bigquery")
def get_articles():

    # lê o sheets
    # salva no bigquery
    # Run -> as 20 horas

    return jsonify({'status': 'success', 'massage': 'etl project newspaper articles about greenpeace brazil'}), 200


if __name__ == "__main__":  # On running python app.py
    app.run(debug=True)
