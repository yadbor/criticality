# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

import socket
from struct import unpack   # to parse UDP packets
from time import time_ns    # high resolution system time. only >= python 3.3

import getopt, sys          # command line arguments

## ------------------ Set up network stuff here ------------------

UDP_IP = '' # localhost
UDP_PORT = [5555]  # could potentially listen on multiple ports

# make a UDP socket & bind it to the chosen port
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT[0]))
buffer_len = 512  # at least bigger than a packet

struct = '<2c2b6f8d19b'
def decode_stream(message):
    packet = unpack(struct, message)
    ax, ay, az = packet[4:7]
    gx, gy, gz = packet[7:10]
    return ax, ay, az, gx, gy, gz

def decode_hyper(message):
    packet = [float(x) for x in message.split(b',')]
    ax, ay, az = packet[0:3]
    gx, gy, gz = packet[3:6]
    return ax, ay, az, gx, gy, gz

def getdata():
    udp_message, udp_client = udp_socket.recvfrom(buffer_len)
    # decode into a bunch of numbers to plot
    channels = decode_data(udp_message)
    return np.array(channels, dtype=np.float)

## ------------------ Set up the data structures ------------------
buffer_length = 500

# only look at acceleration & gyroscope for now
sensors = ['acceleration', 'gyroscope']
nSensors = len(sensors)

# each sensor has three components
nComponents = 3
x,y,z = range(nComponents)  # indices for each component

# make a different coloured pen for each component
pens = [pg.mkPen(width=5, color='wgb'[i]) for i in range(nComponents)]

## after experimentation decided that probably want gyro green (1) and red (0)
## green: gyr_data[y] is spinning around long axis (1)
## red:   gyr_data[x] is leaning back & forward    (0)
## blue:  gyr_data[z] is leaning side to side      (2)
##
## so, only generate two curves & two plots

gyr_y = np.zeros(buffer_length)
gyr_x = np.zeros(buffer_length)

# maybe want the magnitude vector (in the bottom graph)
##gyr_mag = np.sqrt(gyr_x**2 + gyr_y**2)

## ------------------ Set up graphics stuff here ------------------

## make the plot widget to hold the plots
win = pg.GraphicsWindow()
win.setWindowTitle('spinning')
win.showMaximized()

gyr_plot = win.addPlot()
##curve_x = gyr_plot.plot(data=gyr_x, pen=pens[x])
curve_y = gyr_plot.plot(data=gyr_y, pen=pens[y])

##win.nextRow()

##mag_plot = win.addPlot()
##curve_m = mag_plot.plot(data=gyr_mag, pen=pg.mkPen(width=8, color='y'))

## --------------- Set up the update callback functions ---------------
    
startTime = pg.ptime.time()

gyr_plot.setXRange(0, 100)
gyr_plot.setYRange(0, 10)
##mag_plot.setXRange(0, 100)


def update_all():
    global gyr_x, gyr_y, gyr_mag, curve_x, curve_y, curve_mag

    now = pg.ptime.time()
    # get a point from the UDP socket
    this_pt = getdata()

##    gyr_x[1:] = gyr_x[:-1]
##    gyr_x[0] = this_pt[3]  # gx
##    curve_x.setData(gyr_x)

    gyr_y[1:] = gyr_y[:-1]
    gyr_y[0] = this_pt[4]  # gy
    curve_y.setData(gyr_y)

##    gyr_mag = np.sqrt(gyr_x**2 + gyr_y**2)
##    curve_m.setData(gyr_mag)

    
timer = pg.QtCore.QTimer()
timer.timeout.connect(update_all)
timer.start(0)

def usage():
    print("usage:\n\t--hyper to use android phone\n\t--max = max spin")

def set_options():
    global decode_data, max_spin
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:v", ["hyper", "max="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    max_spin = 10
    # choose which method to use
    decode_data = decode_stream

    for o, a in opts:
        if o == "--hyper":
            decode_data = decode_hyper
        elif o in ("-m", "--max"):
            max_spin = int(a)
        else:
            assert False, "unhandled option"
    

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    set_options()
    gyr_plot.setYRange(0, max_spin)

    # zen fire ze missiles...
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

