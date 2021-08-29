# from picam import CameraFunctions
from flask import Flask
import cv2
from imutils.video.pivideostream import PiVideoStream
import time
import numpy as np
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

pi_camera = VideoCamera(flip=False) 
app = Flask(__name__)

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/preview')
def preview(self):
    return Response(gen(pi_camera),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)