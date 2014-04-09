#!/usr/bin/python

from gpsAngleClass import GpsAngle
from gpsClass1 import LocationGPS
from xbeePort0 import SuperXbee
from servo_control import PololuMicroMaestro
import time


class Main(object):
    def __init__ (self):
        self.gpsAngle = GpsAngle()
        # uncomment this when you want to use the gps
        #self.gpsLoc = LocationGPS()
        self.xbee = SuperXbee()
        self.rudder = PololuMicroMaestro()
        self.sails = PololuMicroMaestro()

    # untested function to determine positioning of sails
    def frontalWind(self,destAngle):
        if ((destAngle > 0.0 and destAngle < 30.0) or (destAngle > 150.0 and destAngle < 180.0)):
            self.sails.setAngle(1,75)          ## Sails at 1/4 way in
        if (destAngle == 0.0 or destAngle == 180.0):
            self.sails.setAngle(1,80)          ## Sails at 1/2 way out
        if ((destAngle < 0.0 and destAnlge > -80) or (destAngle < -100.0 and destAngle > -179)):
            self.sails.setAngle(1,85)          ## Sails at 3/4 way out
        if (destAngle > -100 and destAngle < -80):
            self.sails.setAngle(1,90)          ## Sails at all way out, wind comes from the back
        if ((destAngle > 30.0 and destAngle < 35.0) or (destAngle < 150.0 and destAngle > 145.0)):
            self.sails.setAngle(1,70)          ## At the edge of No Go Zone
        if (destAngle > 35.0 and destAngle < 145):
            self.sails.setAngle(1,75)          ## Tacking and driving when the boat it's in No Go Zone
        for i in range(80, 100):
            self.rudder.setAngle(0,i)
            i = i + 5
        for i in range(80,60 ):
            self.rudder.setAngle(0,i)
            i = i - 5


    def mainFunction(self):
        time1 = 0.0
        time2 = 0.0
    ## Read destination from user (self.xbee)
        self.xbee.write("\nLatitude of Destination = ")
        destLat = self.xbee.read(9)
        self.xbee.write("\nLongitude of Destination = ")
        destLong = self.xbee.read(11)
        #inital rudder setup
        rudderAngle = 80
        self.rudder.setAngle(0,rudderAngle)
        while True:
            time2 = time.clock()
        ## Calculate the desired direction to go (Based on angle)
        # destAngle = str(self.gpsAngle.calculateAngle(float(self.gpsLoc.getLatitude()), float(gpsLoc.getLongitude()), float(destLat), float(destLong)))
            #self.gpsLoc.getLocation()
            #print "Latitude: " + str(self.gpsLoc.getLatitude())
            #print "Longitude: " + str(self.gpsLoc.getLongitude())
            
            # hard coded gps coordinates due to being indoors
            destAngle = int(self.gpsAngle.calculateAngle(43.818544, -111.782777, float(destLat), float(destLong)))
            print "destAngle" + str(destAngle)
            direction = self.gpsAngle.getDirectionToHead()
            print "direction: "  + str(direction)
                        
        ## Get actual direction based on the compass
            fi = open("direction.txt", "r")
            currDirection = fi.read(2)
            print "currDirection: " + currDirection
            fi.close()
        ## Get wind direction based on the wind sensor
            fi = open("wind.txt", "r")
            windDirection = fi.read(1)
            print "windDirection: " + windDirection
            fi.close()

        ## Set rudder and set Sails based on wind, current direction, and direction 
            if currDirection == "NO":
                currAngle = 90.0
            if currDirection == "NE":
                currAngle = 45.0
            if currDirection == "NW":
                currAngle = 135.0
            if currDirection == "EA":
                currAngle = 0.0
            if currDirection == "WE":
                currAngle = 180.0
            if currDirection == "SO":
                currAngle = -90.0
            if currDirection == "SE":
                currAngle = -45.0
            if currDirection == "SW":
                currAngle = -135.0
            
    
        ## Calculate the angle the rudder has to rotate
            x = destAngle - currAngle
            if x > 180.0 or x < 0.0:
                if x > 180.00:
                    x = (360.0 - x)
                else:
                    x =  abs(x)
                self.rudder.setAngle(0,(80 + (x / 6)))
            elif x <= 180.0 or x >= 0.0:
                self.rudder.setAngle(0, (80 - (x / 6)))
            
        ## untested code
        ## Calculate the rotation of the sails
            if windDirection == "F":
                frontalWind(destAngle)
            if windDirection == "B":
                if destAngle > -150.0 and destAngle < -30.0:
                    frontalWind(destAngle)
                else:
                    self.sails.setAngle(1,90)
            if (windDirection == "R" or windDirection == "L"):
#            if ((destAngle > 0.0 and destAngle < 60.0) or (destAngle < 0.0 and destAngle > -60.0)):
#                frontalWind(destAngle)
#            else:
                self.sails.setAngle(1,80)
#        if windDirection == "L":
#            if ((destAngle > 120.0 and destAngle < 180) or (destAngle > -120.0 and destAngle < -180.0)):
#                frontalWind(destAngle)
#            else:
#                self.sails.setAngle(1,80)       

        ## Verify if location has been reached (Close enough)
            #latitudeX = float(destLat) - float(self.gpsLoc.getLatitude())
            #longitudeX = float(destLong) - float(self.gpsLoc.getLongitude())
            #if (latitudeX <= 0.09 and longitudeX <= 0.09):
            #    self.xbee.write("\nDestination has been reached")
            #    self.xbee.write("\nLatitude of New Destination = ")
            #    destLat = self.xbee.read(9)
            #    self.xbee.write("\nLongitude of New Destination = ")
            #    destLong = self.xbee.read(11)
            #else:
            #    if ((time2 - time1) >= 60.0):
            #        self.xbee.write("\nMy current location is: \nLatitude = " + self.gpsLoc.getLatitude())
            #        self.xbee.write("\nLongitude = " + self.gpsLoc.getLongitude())

#####
# NOTES:
# 1)  I am not sure if the function needs the parameters of the objects, since they are kind of global
# Tried to find something in python that explains how that works,  but no luck yet
# 2)  I don't want to display the location of the sailboat in every cycle, so we need to make it just show
# where it is after certain period...........
