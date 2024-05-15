from evdev import InputDevice, categorize, ecodes, list_devices
import socket

# List all input devices
devices = [InputDevice(path) for path in list_devices()]
for i, device in enumerate(devices):
    print(f"{i}: {device.path} - {device.name} - {device.phys}")

# Prompt user to select a device
device_index = int(input("Select the device number: "))
selected_device = devices[device_index]

print(f"Listening to {selected_device.path}, {selected_device.name}, {selected_device.phys}")

# Set up UDP socket
UDP_IP = "127.0.0.1"  # Change to the receiver's IP if not running on the same machine
UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Read events from the selected device and send over UDP
for event in selected_device.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        event_data = f"{event.type},{key_event.event.code},{key_event.event.value}"
        sock.sendto(event_data.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent key event: {event_data}")
    elif event.type == ecodes.EV_ABS:
        abs_event = categorize(event)
        event_data = f"{event.type},{abs_event.event.code},{abs_event.event.value}"
        sock.sendto(event_data.encode(), (UDP_IP, UDP_PORT))
        print(f"Sent absolute event: {event_data}")
