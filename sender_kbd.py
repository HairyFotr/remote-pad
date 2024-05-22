import struct
import socket

from evdev import ecodes
from pynput import keyboard

import config

# Mapping keys to gamepad events
key_mapping = {
    'z': (ecodes.EV_KEY, 307, 1),  # X button press
    'x': (ecodes.EV_KEY, 304, 1),  # A button press
    'c': (ecodes.EV_KEY, 305, 1),  # B button press
    'i': (ecodes.EV_KEY, 307, 1),  # X button press
    'o': (ecodes.EV_KEY, 304, 1),  # A button press
    'p': (ecodes.EV_KEY, 305, 1),  # B button press
    'w': (ecodes.EV_KEY, 17, -1),  # D-Pad up press
    'a': (ecodes.EV_KEY, 16, -1),  # D-Pad left press
    's': (ecodes.EV_KEY, 17, -1),  # D-Pad down press
    'd': (ecodes.EV_KEY, 16, -1),  # D-Pad right press
    # 'up': (ecodes.EV_KEY, 17, -1),  # D-Pad up press
    # 'left': (ecodes.EV_KEY, 16, -1),  # D-Pad left press
    # 'down': (ecodes.EV_KEY, 17, -1),  # D-Pad down press
    # 'right': (ecodes.EV_KEY, 16, -1),  # D-Pad right press
    # 'space': (ecodes.EV_KEY, 315, 1),  # Start button press
    # 'enter': (ecodes.EV_KEY, 315, 1)   # Start button press
    'up': (ecodes.EV_KEY, 1, config.JOY_MIN),  # Joystick up press
    'left': (ecodes.EV_KEY, 0, config.JOY_MIN),  # Joystick left press
    'down': (ecodes.EV_KEY, 1, config.JOY_MAX),  # Joystick down press
    'right': (ecodes.EV_KEY, 0, config.JOY_MAX),  # Joystick right press
    'space': (ecodes.EV_KEY, 315, 1),  # Start button press
    'enter': (ecodes.EV_KEY, 315, 1)   # Start button press
}

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_ADDR = (config.UDP_IP, config.UDP_PORT)

def on_press(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = key.name

    if key_char in key_mapping:
        event = key_mapping[key_char]
        sock.sendto(struct.pack(config.STRUCT_FORMAT, event[0], event[1], event[2]), UDP_ADDR)
        if config.PRINT:
            print(event[0], event[1], event[2])

def on_release(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = key.name

    if key_char in key_mapping:
        event = key_mapping[key_char]
        # Send key release event
        sock.sendto(struct.pack(config.STRUCT_FORMAT, event[0], event[1], 0), UDP_ADDR)
        if config.PRINT:
            print(event[0], event[1], 0)


# Start listening to keyboard inputs
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()