import picamera
import io
import cv2
import threading


class FrameGenerator(threading.Thread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.stream = io.BytesIO()
        self.camera.start_recording(self.stream, format='h264')

    def run(self):
        while True:
            frame = self.stream.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def main():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    generator = FrameGenerator(camera)
    generator.start()
    for frame in generator:
        print(frame)


if __name__ == '__main__':
    main()