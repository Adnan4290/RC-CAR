import picamera
import io
import threading

camera = picamera.PiCamera(resolution=(640, 480), framerate=30, format='jpeg')
stream = io.BytesIO()

def capture_frames():
    while True:
        # capture a frame
        camera.capture(stream, format='jpeg', use_video_port=True)
        # signal the main thread to process the captured frame
        event.set()

def gen_frames():
    while True:
        # wait for a new frame to be captured
        event.wait()
        # reset stream for next frame
        stream.seek(0)
        stream.truncate()
        # yield the frame in bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
        # clear the event to signal that the frame has been processed
        event.clear()

# start the background thread to capture frames
event = threading.Event()
thread = threading.Thread(target=capture_frames, daemon=True)
thread.start()
