import struct
import uinput
import socket

import config

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
    uinput.ABS_X + (config.JOY_MIN, config.JOY_MAX, 0, 0),
    uinput.ABS_Y + (config.JOY_MIN, config.JOY_MAX, 0, 0),
    uinput.ABS_RX + (config.JOY_MIN, config.JOY_MAX, 0, 0),
    uinput.ABS_RY + (config.JOY_MIN, config.JOY_MAX, 0, 0),
    uinput.ABS_HAT0X + (-1, 1, 0, 0),  # D-Pad X
    uinput.ABS_HAT0Y + (-1, 1, 0, 0),  # D-Pad Y
]

print("Creating uinput device")
device = uinput.Device(events, name="RemotePad")

# Set up UDP socket
print("Setting up UDP socket")
UDP_ADDR = (config.UDP_BIND_IP, config.UDP_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(UDP_ADDR)

print(f"Listening for UDP packets on {config.UDP_BIND_IP}:{config.UDP_PORT}")
if not config.PRINT:
    print("Warning: Print is off, there will be no output")
while True:
    data, addr = sock.recvfrom(1024)
    event_type, code, value = struct.unpack('BHh', data)
    device.emit((event_type, code), value)
    if config.PRINT:
        print(f"{event_type} {code} {value}")
