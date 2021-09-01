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
            time.sleep(2)
            camera.resolution = (1280, 720)
            camera.shutter_speed = 6000000
            camera.iso = 800
            # a = np.zeros((720, 1280, 3), dtype=np.uint8)
            # a[360, :, :] = 0xff
            # a[:, 640, :] = 0xff
            a = np.zeros((400, 400, 3), dtype=np.uint8)
            camera.add_overlay(a.tobytes(), layer=3, alpha=160)
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'png',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
