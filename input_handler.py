from flask import request
# import RPi.GPIO as GPIO

# Set up GPIO pins
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(16, GPIO.OUT)
# GPIO.setup(20, GPIO.OUT)
# GPIO.setup(21, GPIO.OUT)
# GPIO.setup(26, GPIO.OUT)
# GPIO.setup(19, GPIO.OUT)

# Define button states
button_states = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

# Define speed
speed = 5  # in volts

def handle_input():
    data = request.form
    for key in button_states:
        if key in data:
            button_states[key] = int(data[key])

    # Send data through GPIO pins
    # GPIO.output(16, button_states['up'])
    # GPIO.output(20, button_states['down'])
    # GPIO.output(21, button_states['left'])
    # GPIO.output(26, button_states['right'])
    # GPIO.output(19, speed)
    # GPIO.cleanup()

    # Generate message
    message = ''
    if button_states['up'] == 1:
        message += 'Up button pressed<br>'
    if button_states['down'] == 1:
        message += 'Down button pressed<br>'
    if button_states['left'] == 1:
        message += 'Left button pressed<br>'
    if button_states['right'] == 1:
        message += 'Right button pressed<br>'

    return message

