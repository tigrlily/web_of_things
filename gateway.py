

#!/usr/bin/env python
from flask import Flask, render_template, Response, request
from flask_cors import CORS, cross_origin
from flask import json
import random
import serial_devices
import threading
import logging

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/devices')
def devices():
    return json.jsonify(serial_devices.get_device_data())

@app.route('/add_device')
def add_device():
  type = request.args.get('type', '')

  if type in ['gyro','temp','pressure','led']:
    serial_devices.add_device(type)
    return "OK"
  else:
    return "Not a valid type", 404


if __name__ == '__main__':

    th = threading.Thread(target=serial_devices.run_simulation)
    th.daemon = True
    th.start()
    app.run(host='0.0.0.0', debug=True, threaded=True)
