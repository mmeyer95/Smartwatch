'''
Created by Meredith Meyer
Last Edited 11/30/2019

User inputs:
    -Raw data filename
    -cutoff frequency
'''
filename = r'C:\Users\Meredith\Desktop\Lift_Periodic.txt'
cutOff = 1.66   #filter cutoff frequency - 140 steps/min = jogging
height = -9.0      #min height for peaks

import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqs, filtfilt
from scipy.signal import find_peaks
import math

def butter_lowpass(cutOff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low', analog = False)
    return b, a

def butter_lowpass_filter(data, cutOff, fs, order=4):
    b, a = butter_lowpass(cutOff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def read_data(filename):
    print("\nREADING DATA...")
    raw_data = []
    with open(filename) as fp:
        line = fp.readline()
        while line:
            reading = [""]*4
            i = 0
            inside = True
            for letter in line:
                if letter != "\t":
                    inside = True
                    reading[i] += letter
                elif inside == True and letter == "\t":
                    inside = False
                    i += 1
            raw_data.append(reading)
            line = fp.readline()
    print("DATA READING COMPLETE.")
    return raw_data
    
def display_data(data):
    t = []
    x = []
    y = []
    z = []
    net = []
    for reading in data:
        t.append(int(reading[0]))
        x.append(float(reading[1]))
        y.append(float(reading[2]))
        z.append(float(reading[3]))
        net.append(math.sqrt(x[-1]**2 + y[-1]**2 + z[-1]**2))
    plt.figure()
    plt.title("Raw Accelerometer Data.")
    plt.xlabel("Time(ms)")
    plt.ylabel("Accel(m/s2)")
    plt.plot(t, x, label="X")
    plt.plot(t, y, label="Y")
    plt.plot(t, z, label="Z")
    plt.plot(t, net, label="Vector sum.")
    plt.legend()
    return t, x, y, z, net
    
def low_pass(data, name=None):
    fs = 30.00
    order = 6
    filt_data = [float(i) for i in data]
    y = butter_lowpass_filter(filt_data, cutOff, fs, order)
    plt.figure()
    if name:
        plt.title("Low Pass Filter Output vs. Raw for "+name)
    plt.plot(data, linewidth= 0.5, label="Raw data.")
    plt.plot(y,'r-', linewidth=2, label="Filtered data.")
    plt.legend()
    return y
    
def count_cycles(t, data, name):
    peaks = find_peaks(data, height)
    peaks = peaks[0]
    num_peaks = len(peaks)
    plt.figure()
    plt.title("Filtered Data Displaying "+str(num_peaks)+" Cycles in "+name)
    plt.plot(t, data)
    peak_t = []
    peak_x = []
    for i in peaks:
        peak_t.append(t[i])
        peak_x.append(data[i])
    plt.plot(peak_t,peak_x, 'r*', linewidth=3)
    
def detect_lift(t, data):
    state = [] #watch face off
    on = False
    high = -8.80
    low = -6.00
    for r in data:
        if on:
            state.append(1)
        else:
            state.append(0)
        if not on and r <= high:
            on = True
        if on and r > low:
            on = False
    fig, ax1 = plt.subplots()
    plt.title("Filtered Acceleration and Screen Lit State")
    ax1.plot(t, data, label = "Z")
    ax2 = ax1.twinx()
    ax2.plot(t, state, "r-", label="State")
    plt.show()
            
    
        
        
data = read_data(filename)
t, x, y, z, net = display_data(data)
filt_x = low_pass(x, "X")
filt_y = low_pass(y, "Y")
filt_z = low_pass(z, "Z")
detect_lift(t, filt_x)
filt_net = low_pass(net, "Vector Sum")
count_cycles(t, filt_x, "X")
count_cycles(t, filt_y, "Y")
count_cycles(t, filt_z, "Z")
count_cycles(t, filt_net, "Vector Sum")

