import struct
import socket
import pywinusb.hid as hid

import config


# Helper function to list HID devices
def list_devices():
    all_devices = hid.HidDeviceFilter().get_devices()
    return all_devices

# Helper function to read events from a selected HID device
def read_events(device, callback):
    device.open()
    device.set_raw_data_handler(callback)


# List all input devices
devices = list_devices()
for i, device in enumerate(devices):
    print(f"{i}: {device.vendor_name} - {device.product_name}")

# Prompt user to select a device
device_index = int(input("Select the device number: "))
selected_device = devices[device_index]

print(f"Listening to {selected_device.vendor_name} - {selected_device.product_name}")

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_ADDR = (config.UDP_IP, config.UDP_PORT)

# Callback function to handle HID data and send over UDP
def raw_data_handler(data):
    event_type = data[1]
    code = data[2]
    value = struct.unpack('h', bytes(data[3:5]))[0]
    packed_data = struct.pack(config.STRUCT_FORMAT, event_type, code, value)
    sock.sendto(packed_data, UDP_ADDR)
    print(event_type, code, value)


if not config.PRINT:
    print("Warning: Print is off, there will be no output")

# Read events from the selected device
read_events(selected_device, raw_data_handler)

# Keep the script running
input("Press Enter to exit...\n")
