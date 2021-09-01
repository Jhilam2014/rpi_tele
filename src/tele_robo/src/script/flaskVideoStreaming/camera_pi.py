import io
import time
import picamera
from base_camera import BaseCamera
import numpy as np
from PIL import Image

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)
            camera.resolution = (640,480)
            camera.shutter_speed = 600000
            camera.iso = 800
            camera.framerate = 24
            
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'png',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
