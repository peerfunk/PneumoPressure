import time
import socket
import math
from collections import deque , defaultdict
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import threading
from statistics import *
import numpy as np
from scipy.signal import butter, lfilter, freqz, argrelextrema
from mulicastconnector import *

#http://electronut.in/plotting-real-time-data-from-arduino-using-python/
order = 6
fs = 10.0       # sample rate, Hz
cutoff = 3  # desired cutoff frequency of the filter, Hz

class DataPlot:
    run = True
    
    def __init__(self, max_entries = 100):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.max_entries = max_entries
        self.buf1=deque(maxlen=100)
        self.conmgr = connectionMan(self)
        
    def add(self, x, y):
        self.axis_x.append(int(x))
        self.axis_y.append(int(y))
        fh = open("measurements.csv","a")
        fh.write((str(y)+ ";"+str(x) + "\n"))
        fh.close()    
    def getData(self):
        return (butter_lowpass_filter(self.axis_y, cutoff, fs, order))
    def getRaw(self):
        return self.axis_y
    def getMin(self):
        return  np.nan_to_num(argrelextrema(np.array((self.axis_y)), np.less,0 , 5))
    def getMax(self):
        return  np.nan_to_num(argrelextrema(np.array((self.axis_y)), np.greater,0 , 5))
    def getYForIndizes(self, indizes):
        a = []
        for index in indizes:
        #   if index == "nan"  or index == None:
        #       index = 0
            a.append(self.axis_y[index])
        return np.nan_to_num(a)
    def getYForIndex(self,index):
        if index == "nan":
            index = 0
        return self.axis_y[index]
    def recData(self):
        port = 5005
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", port))
        count=0
        while(self.run):
          count+=1
          rec, addr = s.recvfrom(1024)
          self.add(count,int(rec.decode()))
class RealtimePlot:
    def __init__(self, axes):
        self.axes = axes
        self.lineplot, = axes.plot([], [], "-")
        self.minplot, = axes.plot([],[],"x")
        self.maxplot, = axes.plot([],[],"o")
        
        self.axes.set_ylim(0,1000)
        self.axes.relim()
        
        
    def plot(self, dataPlot):
        
        axis_y = dataPlot.getRaw()
        if(len(axis_y)>0):
            #print("maxima: " + str(argrelextrema(axis_y, np.greater)))
            self.lineplot.set_data(dataPlot.axis_x, axis_y)
            self.axes.set_xlim(min(dataPlot.axis_x), max(dataPlot.axis_x))
            #self.minplot.set_data(dataPlot.axis_x[0]+dataPlot.getMin()[0],dataPlot.getYForIndizes(dataPlot.getMin()[0]))
            #self.maxplot.set_data(dataPlot.axis_x[0]+dataPlot.getMax()[0],dataPlot.getYForIndizes(dataPlot.getMax()[0]))
            
            self.axes.relim();
            mini =0
            maxi = 0
            #mini = str(np.nan_to_num(np.mean(dataPlot.getYForIndizes(dataPlot.getMin()[0]))))
            #maxi = str(np.nan_to_num(np.mean(dataPlot.getYForIndizes(dataPlot.getMax()[0]))))
            #self.fh.write(str(axis_y[0]) +";" + str(mini) + ";" + str(maxi)+ "\n")
            #print(str(axis_y[0]) + "\n")
           
            
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def main():
    fig, axes = plt.subplots()
    
    plt.title('Plotting Data')
    data = DataPlot();
    cid = fig.canvas.mpl_connect('button_press_event',data.getMin)
    dataPlotting= RealtimePlot(axes)
    plt.pause(1)
    try:
        while True:
            dataPlotting.plot(data)
            #print(data.axis_y)
            plt.pause(0.001)
    except KeyboardInterrupt:
        print('nnKeyboard exception received. Exiting.')
        plt.close()
        data.run = False
        data.getMin()
        exit()

if __name__ == "__main__": main()
