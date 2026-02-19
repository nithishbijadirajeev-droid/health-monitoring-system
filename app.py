from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'healthdb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vitals (
            id SERIAL PRIMARY KEY,
            patient_name VARCHAR(100),
            heart_rate INTEGER,
            blood_pressure VARCHAR(20),
            temperature FLOAT,
            status VARCHAR(20),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Health Monitoring System</title>
    <style>
        body { font-family: Arial; background: #f0f4f8; padding: 30px; }
        h1 { color: #2c3e50; text-align: center; }
        .container { max-width: 800px; margin: auto; }
        .form-box { background: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { background: #3498db; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background: #2980b9; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        th { background: #3498db; color: white; padding: 12px; text-align: left; }
        td { padding: 10px 12px; border-bottom: 1px solid #eee; }
        .normal { color: green; font-weight: bold; }
        .warning { color: orange; font-weight: bold; }
        .critical { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Health Monitoring System</h1>
        <div class="form-box">
            <h3>Submit Patient Vitals</h3>
            <form method="POST" action="/submit">
                <input type="text" name="patient_name" placeholder="Patient Name" required/>
                <input type="number" name="heart_rate" placeholder="Heart Rate (bpm)" required/>
                <input type="text" name="blood_pressure" placeholder="Blood Pressure (e.g. 120/80)" required/>
                <input type="number" step="0.1" name="temperature" placeholder="Temperature (F)" required/>
                <button type="submit">Submit Vitals</button>
            </form>
        </div>
        <h3>Patient Records</h3>
        <table>
            <tr><th>Patient</th><th>Heart Rate</th><th>Blood Pressure</th><th>Temperature</th><th>Status</th><th>Time</th></tr>
            {% for row in records %}
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }} bpm</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }} F</td>
                <td class="{{ row[5] }}">{{ row[5].upper() }}</td>
                <td>{{ row[6].strftime("%Y-%m-%d %H:%M") }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM vitals ORDER BY timestamp DESC LIMIT 20')
        records = cur.fetchall()
        cur.close()
        conn.close()
    except:
        records = []
    return render_template_string(HTML, records=records)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['patient_name']
    hr = int(request.form['heart_rate'])
    bp = request.form['blood_pressure']
    temp = float(request.form['temperature'])
    if hr < 60 or hr > 100 or temp > 99.5:
        status = 'critical' if hr > 120 or temp > 103 else 'warning'
    else:
        status = 'normal'
    app.logger.info(f"Patient {name} submitted vitals - Status: {status}")
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO vitals (patient_name, heart_rate, blood_pressure, temperature, status) VALUES (%s, %s, %s, %s, %s)',
                (name, hr, bp, temp, status))
    conn.commit()
    cur.close()
    conn.close()
    return index()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
