import io
import time
import picamera
from fractions import Fraction
from base_camera import BaseCamera
import numpy as np

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            camera.resolution = (1920, 1080)
            camera.shutter_speed = 6*10**5
            test_shutter_speed = camera.exposure_speed
            camera.iso = 800
            camera.awb_mode = "off"
            camera.framerate = 1/9
            camera.awb_gains = 2.0
            time.sleep(2)
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
                print(test_shutter_speed)