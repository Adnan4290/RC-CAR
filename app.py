from flask import Flask, render_template, Response
from camera_stream import gen_frames
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

latitude = None
longitude = None


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/control', methods=['POST'])
def control():
    # handle_input function not defined in your code
    message = "control request received"
    print(message)
    return message


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/switch_camera', methods=['POST', 'GET'])
def switchcamera():
    print("switch camera route accessed")
    # Call the function to switch cameras
    # switch_camera()
    return "switch camera route finished running"


@app.route('/latitude')
def get_latitude():
    global latitude
    return str(latitude)


@app.route('/longitude')
def get_longitude():
    global longitude
    return str(longitude)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def send_frame():
    while True:
        for frame in gen_frames():
            socketio.emit('frame', frame, broadcast=True)


if __name__ == '__main__':
    socketio.start_background_task(target=send_frame)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)