#main.py

#tkinter tutorial: https://www.geeksforgeeks.org/python-tkinter-tutorial/?ref=lbp
#MCP3008 tutorial: https://tutorials-raspberrypi.com/mcp3008-read-out-analog-signals-on-the-raspberry-pi/

import time
import math
import sys
import random
from tkinter import *
import threading
import MCP3008 #MCP3008 class that I found on a forum thread somewhere (modified a bit). It works, just install the SpiDev python package.
import RPi.GPIO as gpio

colors = ["red", "orange", "yellow", "green", "blue", "purple", "black"]
resetWindow = False #flag for resetting the window canvas

if len(sys.argv) > 2:
    dimensions = int(sys.argv[1])
    color = sys.argv[2]
elif len(sys.argv) > 1:
    dimensions = int(sys.argv[1])
    color = "black"
else:
    dimensions = 1000
    color = "black"

gpio.setmode(gpio.BOARD) #set pins to the board pins and not the logical pins on the SOC
gpio.setWarnings(False)
gpio.setup(22, gpio.IN) #the button to reset/clear the screen (reset)

potX = MCP3008(0) #0 is the channel on the ADC. See tutorial for more info.
potY = MCP3008(1)
potXLast = potX.read() #set initial values for the pots
potYLast = potY.read()
threshold = 10 #the threshold for the pots (if they changed more than the threshold, then draw something)

cursorPos = lambda val : (1023/dimensions) * val #this returns the position of where the rectangle should be drawn. it is the proportion : potMaxVal/dimensions = potCurrVal/pos

def drawer(): #main drawing thread
    if (potXLast - threshold) > potX.read() > (potXLast + threshold) || (potYLast - threshold) > potY.read() > (potYLast + threshold): #if the current pot readings are out threshold
        if color == "0": #randomize the color
            random.shuffle(colors)
            color = colors[0]
        canvas.create_rectangle(cursorPos(potX.read()), cursorPos(potY.read()), 
                                cursorPos(potX.read()) + 4, cursorPos(potY.read()) + 4, fill = color)
        potXLast = potX.read()
        potYLast = potY.read()
    if resetWindow:
        canvas.delete('all') #clears all of the widgets inside the canvas
    time.sleep(0.001) #slow the loop a bit

def resetCallback():
    resetWindow = True

gpio.add_event_detect(22, gpio.RISING, callback=resetCallback)  # add rising edge detection on a channel

drawer = threading.Thread(target = drawer, args = (,)) #the thread for actually drawing things in the window.

window = Tk()
window.title("Etch-A-Sketch")
window.geometry(dimensions + "x" + dimensions)

canvas = Canvas(window, bg = "white", height = dimensions, width = dimensions) #makes a canvas with a white background the same dimensions as the screen

canvas.pack() #packs all of the "widgets" into the window
window.mainloop()
gpio.cleanup()