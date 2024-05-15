import uinput
import time
import socket

from evdev import ecodes

# Define the buttons and axes for the virtual gamepad
events = [
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_SELECT,
    uinput.BTN_START,
    uinput.BTN_MODE,  # Home button
    uinput.BTN_TL,    # LB
    uinput.BTN_TR,    # RB
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (-32768, 32767, 0, 0),
    uinput.ABS_Y + (-32768, 32767, 0, 0),
    uinput.ABS_RX + (-32768, 32767, 0, 0),
    uinput.ABS_RY + (-32768, 32767, 0, 0),
    uinput.ABS_HAT0X + (-1, 1, 0, 0),  # D-Pad X
    uinput.ABS_HAT0Y + (-1, 1, 0, 0),  # D-Pad Y
]

print("Creating uinput device")
device = uinput.Device(events)

# Set up UDP socket
UDP_IP = "0.0.0.0"
UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on port {UDP_PORT}")
while True:
    data, addr = sock.recvfrom(1024)
    event_type, code, value = data.decode().split(',')
    event_type = int(event_type)
    code = int(code)
    value = int(value)

    if event_type in (ecodes.EV_KEY, ecodes.EV_ABS):
        print(f"Received {event_type} {code} {value}")
        device.emit((event_type, code), value)