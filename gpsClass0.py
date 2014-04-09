#!/usr/bin/python

import serial

class LocationGPS(object):
    latitude = ""
    longitude = ""
    speed = ""
    course = ""
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 4800, timeout = 1)
        print "In Constructor"
    def getLocation(self):
        #self.ser = serial.Serial('/dev/ttyUSB0', 4800, timeout = 1)
        x = self.ser.read(1200) #Get raw GPS data
        if x != "":
            # retrieves data in DDMM.MMMM format
            pos1 = x.find("$GPRMC")
            pos2 = x.find("\n", pos1)
            loc = x[pos1:pos2]
            data = loc.split(',')
            if data[2] == 'V':
                print "No location found"
            else:
                # calculations to convert DDMM.MMMM to decimal deg
                tempLat = str(data[3])
                tempLat1 = tempLat[2:9]
                tempLat = tempLat[0:2]
                tempLat = float(tempLat) + float(tempLat1) / 60.0  
                LocationGPS.latitude = tempLat
		tempLong = str(data[5])
                tempLong1 = tempLong[3:10]
                tempLong = tempLong[0:3]
                tempLong = float(tempLong) + float(tempLong1) / 60.0
                # temporary solution as it only works on this hemisphere, hence the negative longitude
                LocationGPS.longitude = -tempLong
                LocationGPS.speed = " Speed = " + data[7]
                LocationGPS.course = "Course = " + data[8] + "\n"
                #return LocationGPS.latitude + LocationGPS.longitude + LocationGPS.speed + LocationGPS.course
    def getLatitude(self):
        self.getLocation()
        return LocationGPS.latitude
    def getLongitude(self):
        self.getLocation()
        return LocationGPS.longitude
    def getSpeed(self):
        self.getLocation()
        return LocationGPS.speed
    def getCourse(self):
        return LocationGPS.course
    def close(self):
        self.ser.close()

if __name__=="__main__":
    locGps = LocationGPS()
    locGps.getLocation()
