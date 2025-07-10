from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

DATA_FILE = 'data.json'

# Betöltjük az adatokat fájlból vagy inicializálunk
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
else:
    data = {
        "Bőrgyógyászat": [],
        "Szemészet": [],
        "Urológia": []
    }

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return "Beteghívó rendszer"

@app.route('/input')
def input_page():
    return render_template('input.html', options=list(data.keys()))

@app.route('/display')
def display_page():
    return render_template('display.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html', options=list(data.keys()))

@app.route('/add_number', methods=['POST'])
def add_number():
    content = request.json
    option = content.get('option')
    number = content.get('number')
    if option in data:
        data[option].append(number)
        save_data()
        socketio.emit('update', data)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "message": "Invalid option"}), 400

@app.route('/call_number', methods=['POST'])
def call_number():
    content = request.json
    option = content.get('option')
    number = content.get('number')
    if option in data and number in data[option]:
        data[option].remove(number)
        save_data()
        socketio.emit('update', data)
        socketio.emit('call', {"option": option, "number": number})
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "message": "Invalid option or number"}), 400

@socketio.on('connect')
def handle_connect():
    emit('update', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
