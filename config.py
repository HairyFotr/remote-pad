UDP_PORT = 8888
UDP_IP = "127.0.0.1"  # Change to the receiver's IP if not running on the same machine
UDP_BIND_IP = "0.0.0.0"
JOY_MIN, JOY_MAX = 0, 512  # Generic
JOY_MIN, JOY_MAX = -32768, 32767  # Xbox
STRUCT_FORMAT = 'BHh'  # Xbox, can probably be less on 2 or 3 for Generic, see: https://docs.python.org/3/library/struct.html
PRINT = False