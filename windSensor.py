#!/usr/bin/env python

# Note: This code was mostly found online, and then we turned it into a class.

#Basic imports
from ctypes import *
import sys
import random
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit

# This is basically an analog to digital converter that tells you the current wind speed on the wind sensor.
class WindSensor(object):
    interfaceKit = 0
    e_param = 0
    # Initialize the phidget.
    def __init__(self):
        try:
            print("Hi")
            WindSensor.interfaceKit = InterfaceKit()
        except RuntimeError as e:
            print("Runtime Exception: %s" % e.details)
            print("Exiting....")
            exit(1)
    #Information Display Function
    def displayDeviceInfo(self):
        print("|Attached: %s |Type: %s |Serial #: %d |Version:%d |" % (WindSensor.interfaceKit.isAttached(), WindSensor.interfaceKit.getDeviceName(), WindSensor.interfaceKit.getSerialNum(), WindSensor.interfaceKit.getDeviceVersion()))

    #Event Handler Callback Functions
    def interfaceKitError(self,e):
        try:
            source = e.device
            print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
    # The value has changed. Print if you'd like.                
    def interfaceKitSensorChanged(self,e):
        source = e.device
        WindSensor.e_param = e
        #print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))
    # Set up the phidget and start it running.
    def run(self):
        chr = sys.stdin.read(1)
        print("Closing...")
        try:
            WindSensor.interfaceKit.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)
        print("Done.")
    # Get the current value on the converter.
    def getValue(self):
        return WindSensor.e_param.value
    # Start everything up and get it running and publishing data. When there is an error, publish it to the command line.
    def startup(self):
        try:
            WindSensor.interfaceKit.setOnErrorhandler(self.interfaceKitError)
            WindSensor.interfaceKit.setOnSensorChangeHandler(self.interfaceKitSensorChanged)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        print("Opening phidget object....")
        try:
            WindSensor.interfaceKit.openPhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        print("Waiting for attach....")

        try:
            WindSensor.interfaceKit.waitForAttach(10000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            try:
                WindSensor.interfaceKit.closePhidget()
            except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))
                print("Exiting....")
                exit(1)
            print("Exiting....")
            exit(1)
        else:
            self.displayDeviceInfo()

        print("Setting the data rate for each sensor index to 4ms....")
        for i in range(WindSensor.interfaceKit.getSensorCount()):
            try:
                WindSensor.interfaceKit.setDataRate(i, 4)
            except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))

        print("Press Enter to quit....")
    def close(self):
        exit(1)
