import picamera
import io
import cv2


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
stream = io.BytesIO()
camera.start_recording(stream, format='h264')


def gen_frames():
    while True:
        # Read the next frame from the stream
        stream.seek(0)
        data = stream.read()
        frame = bytearray(data)

        # Convert the frame to a format that OpenCV can handle
        img = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), 1)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Yield the frame to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')