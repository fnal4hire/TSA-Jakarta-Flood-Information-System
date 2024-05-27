from flask import Flask, render_template, send_file, jsonify
from data_scraper import scrape_floodgate_data, create_floodgate_graph
import schedule
import time
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/floodgate_table')
def floodgate_table():
    with open('floodgate_data.html', 'r', encoding='utf-8') as file:
        table_html = file.read()
    return table_html

@app.route('/floodgate_graph/<pintu_air>')
def floodgate_graph(pintu_air):
    buf = create_floodgate_graph(pintu_air)
    return send_file(buf, mimetype='image/png')

@app.route('/floodgate_data/<pintu_air>')
def floodgate_data(pintu_air):
    filename = f'{pintu_air.replace(" ", "_")}.csv'
    data = []
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data.append(headers)
            for row in reader:
                data.append(row)
    return jsonify({"headers": data[0], "data": data[1:]})

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scrape_floodgate_data()
    schedule.every(1).hours.do(scrape_floodgate_data)
    threading.Thread(target=run_schedule).start()
    app.run(debug=True)