import io
import time
import picamera
from fractions import Fraction
from base_camera import BaseCamera
import numpy as np

class Camera(BaseCamera):
    @staticmethod
    def frames(**parameters):
        shutterSpeed = parameters.get('shutter_speed',5)
        frameRate = parameters.get('frame_rate',9)
        with picamera.PiCamera() as camera:
            print ('<==',shutterSpeed,frameRate)
            camera.resolution = (1920, 1080)
            camera.shutter_speed = 10*10**int(shutterSpeed)
            camera.iso = 800
            camera.awb_mode = "off"
            try:
                camera.framerate = frameRate
            except Exception as error:
                print(error)
                camera.framerate = 1/6
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