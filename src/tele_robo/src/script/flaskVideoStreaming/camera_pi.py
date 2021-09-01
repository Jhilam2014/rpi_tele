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
            camera.resolution = (640, 400)
            camera.shutter_speed = 6000000
            camera.iso = 800
            camera.annotate_text = '+'

            a = np.zeros((400, 640, 3), dtype=np.uint8)
            a[360, :, :] = 0xff
            a[:, 640, :] = 0xff

            o = camera.add_overlay(a.tobytes(),format='rgba', size=(640,400), window =(10,72,640,400),fullscreen = False)
            o.alpha=64
            o.layer=3



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
