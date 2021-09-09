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
            camera.shutter_speed = 6*10**5
            
            camera.iso = 800
            camera.current_analog_gain = 12.0
            camera.current_awb_mode = "off"
            camera.drc = 'high'
            camera.framerate = 6
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