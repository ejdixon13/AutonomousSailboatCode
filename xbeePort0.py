#!/usr/bin/python

# " " '

import serial

class SuperXbee(object):
    # sets up port that the Xbee is plugged in to.
    def __init__ (self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    
    # function that allows for continuous communication between
    # two Xbee devices
    def startup(self):
        x = 'n'
        while x != 'q':
            x = self.ser.read(5) # read 5 characters from other computer
            self.ser.write("Hello") # write Hello to other computer
            print x # print message retrieved from other computer
    
    # method to write to the other computers screen
    def write(self, message):
        self.ser.write(message)

    # method to read from the other computer based on a message size
    def read(self, messageLen):
        x = ""
        while x == "":
            for i in range(0,messageLen):  ## Give time to read
                x = x + self.ser.read(messageLen)
            return x

    def close(self):
        self.ser.close()
