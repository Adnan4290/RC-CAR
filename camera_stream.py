import picamera
import io

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.format = 'jpeg'  # set format to JPEG
stream = io.BytesIO()

def gen_frames():
    try:
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            # reset stream for next frame
            stream.seek(0)
            stream.truncate()

            # yield the frame in bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
    finally:
        camera.close()
       
