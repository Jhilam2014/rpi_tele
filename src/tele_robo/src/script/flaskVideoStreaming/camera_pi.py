import io
import time
import picamera
from fractions import Fraction
from base_camera import BaseCamera
import numpy as np

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera(resolution=(4056, 3040), framerate=Fraction(1, 6)) as camera:
            # let camera warm up
            camera.resolution = (640, 480)
            camera.shutter_speed = 6*10**5
            
            camera.iso = 800
            camera.awb_mode = "off"
            camera.framerate = 6
            time.sleep(10)
            # camera.exposure_mode = 'off'
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()