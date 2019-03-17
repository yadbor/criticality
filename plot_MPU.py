import sys
import socket
import struct
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import threading
##from statsmodels.nonparametric.smoothers_lowess import lowess

# def main():
global dataList
dataList = [0.0, 0.0, 0.0,  0.0, 0.0, 0.0]

sv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Use the IP address printed from the Arduino here
sv.bind(("", 5555))

# setup_Vis()

# def setup_Vis():
#     global ax, ay, az, gx, gy, gz, yaw, roll, pitch, ptr

ptr = 0
win = pg.GraphicsWindow()
win.setWindowTitle('MPU Data')

p1 = win.addPlot()
p2 = win.addPlot()
p3 = win.addPlot()
win.nextRow()
p4 = win.addPlot()
p5 = win.addPlot()
p6 = win.addPlot()
# win.nextRow()
# p7 = win.addPlot()
# p8 = win.addPlot()
# p9 = win.addPlot()

ax = np.zeros(100)
ay = np.zeros(100)
az = np.zeros(100)
gx = np.zeros(100)
gy = np.zeros(100)
gz = np.zeros(100)
# yaw = np.zeros(100)
# roll = np.zeros(100)
# pitch = np.zeros(100)

# global curve1, curve2, curve3, curve4, curve5, curve6, curve7, curve8, curve9

curve1 = p1.plot(ax)
curve2 = p2.plot(ay)
curve3 = p3.plot(az)
curve4 = p4.plot(gx)
curve5 = p5.plot(gy)
curve6 = p6.plot(gz)
# curve7 = p7.plot(yaw)
# curve8 = p8.plot(roll)
# curve9 = p9.plot(pitch)

def updatePlots():
    global dataList

    # new data scrolls in from Right    
##    ax[:-1] = ax[1:] 
##    ax[-1] = dataList[0]
##    ay[:-1] = ay[1:]
##    ay[-1] = dataList[1]
##    az[:-1] = az[1:]
##    az[-1] = dataList[2]
##    gx[:-1] = gx[1:]
##    gx[-1] = dataList[3]
##    gy[:-1] = gy[1:]
##    gy[-1] = dataList[4]
##    gz[:-1] = gz[1:]
##    gz[-1] = dataList[5]

    # new data scrolls in from Left
    ax[1:] = ax[:-1]
    ax[0] = dataList[0]
    ay[1:] = ay[:-1]
    ay[0] = dataList[1]
    az[1:] = az[:-1]
    az[0] = dataList[2]
    gx[1:] = gx[:-1]
    gx[0] = dataList[3]
    gy[1:] = gy[:-1]
    gy[0] = dataList[4]
    gz[1:] = gz[:-1]
    gz[0] = dataList[5]

    # yaw[:-1] = yaw[1:]
    # yaw[-1] = dataList[6]
    # roll[:-1] = roll[1:]
    # roll[-1] = dataList[7]
    # pitch[:-1] = pitch[1:]
    # pitch[-1] = dataList[8]


    curve1.setData(ax)
    curve2.setData(ay)
    curve3.setData(az)
    curve4.setData(gx)
    curve5.setData(gy)
    curve6.setData(gz)
    # curve7.setData(yaw)
    # curve8.setData(roll)
    # curve9.setData(pitch)

    global ptr
    ptr += 1

##    curve1.setPos(ptr, 0)
##    curve2.setPos(ptr, 0)
##    curve3.setPos(ptr, 0)
##    curve4.setPos(ptr, 0)
##    curve5.setPos(ptr, 0)
##    curve6.setPos(ptr, 0)
    # curve7.setPos(ptr, 0)
    # curve8.setPos(ptr, 0)
    # curve9.setPos(ptr, 0)


def getData():
    """
    This may need to be updated to work properly.
    Such as in the struct.unpack call, number of floats may not be corrected
    """
    global dataList, filterData
##    filterData = np.zeros((5,9))
##    count = 0
    while (True):
        data = sv.recv(1024)
        # print(data)
        dataList = struct.unpack('<2c2b6f8d19b', data)[4:10]
        # print(dataList)
##        while count < 5:
##            filterData[count][:] = np.asarray(dataList[:9])
##            count+=1
##        filterData[:-1] = filterData[1:]
##        filterData[-1][:] = dataList[:9]

t = threading.Thread(target=getData)
t.start()
timer = pg.QtCore.QTimer()
timer.timeout.connect(updatePlots)
timer.start(50)



if __name__ == "__main__":
    import sys
    # main()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtGui.QApplication
        sys.exit(app.instance().exec_())
        
    
