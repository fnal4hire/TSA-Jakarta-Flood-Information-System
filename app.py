from flask import Flask, render_template, jsonify, send_file
import csv
import matplotlib.pyplot as plt
from io import BytesIO

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('floodgate_data')
def floodgate_data():
    with open('floodgate_data.csv', mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = [row for row in reader]
    return jsonify({'headers': headers, 'data': data})

@app.route('/floodgate_html')
def floodgate_html():
    with open('floodgate_data.html', 'r') as file:
        html_content = file.read()
    return jsonify({'html': html_content})

@app.route('/floodgate_graph')
def floodgate_graph():
    timestamps, heights = [], []
    with open('floodgate_data.csv', mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            timestamps.append(row[0])
            heights.append(float(row[1]))

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, heights, marker='o')
    plt.title('Floodgate Height Over Time')
    plt.xlabel('Time')
    plt.ylabel('Height (cm)')
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)