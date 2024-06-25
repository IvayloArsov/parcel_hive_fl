import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import serial
import cv2
import sqlite3
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

serial_port = '/dev/ttyUSB0'
baud_rate = 9600
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.serialutil.SerialException as e:
    print(f"Error opening serial port: {e}")
    #TODO: handle this exception
    ser = None


def init_db():
    """
    Initialize SQLite database with mouse_data table if it doesn't exist yet.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""        
        CREATE TABLE IF NOT EXISTS mouse_data(
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_to_db(x, y, image_path):
    """
    Saves mouse coordinates(x,y) and image's path to database.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO mouse_data(x, y, image_path)
            VALUES (?, ?, ?)''',
                   (x, y, image_path))
    conn.commit()
    conn.close()


def read_serial_data():
    """
    Reads data from serial port and emits to the connected client.
    """
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            socketio.emit('serial_data', {'data': data})
        time.sleep(0.1)


def capture_image():
    """
    Captures image with the default webcam.
    Creates directory if it doesn't exist yet.
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        image_dir = 'static/images'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_path = f'{image_dir}/{time.time()}.jpg'
        cv2.imwrite(image_path, frame)
    cap.release()
    return image_path


serial_thread = threading.Thread(target=read_serial_data)
serial_thread.daemon = True
serial_thread.start()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('mouse_event')
def handle_mouse_event(json):
    """
    Handles mouse events - capture image on left click and saves it to database.
    """
    x = json['x']
    y = json['y']

    if json['click']:
        image_path = capture_image()
        save_to_db(x, y, image_path)
        emit('mouse_response', {
            'x': x,
            'y': y,
            'image_path': image_path
        })
    else:
        #TODO: remove before publishing, using this only for testing functionality
        print(f'Mouse moved to: ({x}, {y}) (non-click)')


if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True)
