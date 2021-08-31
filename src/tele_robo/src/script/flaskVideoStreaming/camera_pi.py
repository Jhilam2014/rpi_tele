import io
import time
import picamera
from base_camera import BaseCamera
from PIL import Image

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)
            camera.shutter_speed = 6000000
            camera.iso = 800
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
            o = camera.add_overlay(pad.tostring(), size=img.size)
            # By default, the overlay is in layer 0, beneath the
            # preview (which defaults to layer 2). Here we make
            # the new overlay semi-transparent, then move it above
            # the preview
            o.alpha = 128
            o.layer = 3
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
