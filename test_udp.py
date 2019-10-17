import socket               # for network access

from struct import unpack   # to parse UDP packets
#from time import time_ns    # high resolution system time. only >= python 3.3

# set up UDP socket listener on my port 5555
host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

# Define the Sensor Stream data packet (Little Endian)
# header    4 bytes
#   magic       2 bytes 'FS'
#   version     1 byte
#   body size   1 byte   107
# accel     3 x float
# gyro      3 x float
# tesla     3 x double
# heading   2 x double
# location  3 x double
# touchpad  19 bytes
struct = '<2c2b6f8d19b'

def decode_stream(message):
    packet = unpack(struct, message)
    magic = packet[:2] # first two bytes should be 'FS'
    version, length = packet[2:4]
    print(length, len(message)-4)
    ax, ay, az = packet[4:7]
    gx, gy, gz = packet[6:9]
    return ax, ay, az, gx, gy, gz

def decode_imu(message):
    # split records using comma as delimiter (data are streamed in CSV format)
        data = message.split( "," )
    # convert to float for plotting purposes
        t = data[0]
        sensorID = int(data[1])
        if sensorID==3:     # sensor ID for the accelerometer
            ax, ay, az = data[2:5]

print("listening on port", port)
while 1:
    try:
        message, address = s.recvfrom(512)
        print(decode_stream(message))
    except (KeyboardInterrupt, SystemExit):
        s.close()
        raise
    except:
        traceback.print_exc()
