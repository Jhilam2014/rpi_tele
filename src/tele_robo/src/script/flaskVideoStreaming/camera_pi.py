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
            # a = np.zeros((720, 1280, 3), dtype=np.uint8)
            # a[360, :, :] = 0xff
            # a[:, 640, :] = 0xff
            # Load the arbitrarily sized image
            img = Image.open('overlay.png')
            # Create an image padded to the required size with
            # mode 'RGB'
            pad = Image.new('RGB', (
                ((img.size[0] + 31) // 32) * 32,
                ((img.size[1] + 15) // 16) * 16,
                ))
            # Paste the original image into the padded one
            pad.paste(img, (0, 0))

            # Add the overlay with the padded image as the source,
            # but the original image's dimensions
            o = camera.add_overlay(pad.tobytes(), size=img.size)
            o.alpha = 128
            o.layer = 3
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'png',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
