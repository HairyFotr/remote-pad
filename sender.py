import struct
import socket
from evdev import InputDevice, categorize, ecodes, list_devices

import config

# List all input devices
devices = [InputDevice(path) for path in list_devices()]
for i, device in enumerate(devices):
    print(f"{i}: {device.path} - {device.name} - {device.phys}")

# Prompt user to select a device
device_index = int(input("Select the device number: "))
selected_device = devices[device_index]

print(f"Listening to {selected_device.path}, {selected_device.name}, {selected_device.phys}")

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_ADDR = (config.UDP_IP, config.UDP_PORT)

if not config.PRINT:
    print("Warning: Print is off, there will be no output")

# Read events from the selected device and send over UDP
for event in selected_device.read_loop():
    if event.type == ecodes.EV_ABS or event.type == ecodes.EV_KEY:
        key_event = categorize(event).event
        sock.sendto(struct.pack(config.STRUCT_FORMAT, event.type, key_event.code, key_event.value), UDP_ADDR)
        if config.PRINT:
            print(event.type, key_event.code, key_event.value)
