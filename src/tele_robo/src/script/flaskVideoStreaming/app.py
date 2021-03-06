#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

app = Flask(__name__)

ss = 1
fr = 1
@app.route('/')
def index():
    """Video streaming home page."""
    args = request.args
    global ss,fr
    ss = args['ss']
    fr = args['fr']
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    global ss,fr
    """Video streaming route. Put this in the src attribute of an img tag."""
    print("==>",ss,fr)
    return Response(gen(Camera(shutter_speed=int(ss),frame_rate=int(fr))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
