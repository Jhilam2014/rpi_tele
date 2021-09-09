import io
import time
import picamera
from base_camera import BaseCamera
import numpy as np

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            camera.resolution = (640, 480)
            camera.shutter_speed = 60000000
            
            camera.iso = 800

            camera.framerate = 12
            time.sleep(10)
            camera.exposure_mode = 'off'
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()