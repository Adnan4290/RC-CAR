import picamera
import io
import cv2


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
stream = io.BytesIO()
# camera.start_preview()


def gen_frames():
    while True:
        success, frame = cv2.VideoCapture(0)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
