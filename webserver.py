from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM temperature ORDER BY date DESC LIMIT 1")
    data = c.fetchone()
    conn.close()
    return jsonify({'date': data[0], 'temp': data[1]})


@app.route('/api/temperature', methods=['GET'])
def api_get_temperature():
    return data()

if __name__ == '__main__':
    app.run(debug=True)
