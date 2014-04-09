#Calculates angle to go from two gps coordinates
import math

class GpsAngle(object):
	def __init__ (self):
		self.angle = 0 # initiate instance variable
	
	# this function uses some trigonometry to calculate the direction
	# angle to head based off of a source and destination coordinates
	# a return value of 90 means to head North
	def calculateAngle(self, sourceLat, sourceLong, destLat, destLong):
		dy = (destLat - sourceLat)
		dx = math.cos((math.pi/180)*sourceLat)*(destLong - sourceLong)
		angle = math.atan2(dy, dx)
		self.angle = math.degrees(angle)
		return self.angle
	# converts degrees to easy to read cardinal directions
	def getDirectionToHead(self):
		if self.angle > 0:
			if ((self.angle > 0.0) and (self.angle < 10.0)):
				return "E"
			if ((self.angle > 10.0) and (self.angle < 80.0)):
				return "NE"
			if ((self.angle > 80.0) and (self.angle < 110.0)):
				return "N"
			if ((self.angle > 110.0) and (self.angle < 170.0)):
				return "NW"
			if ((self.angle > 170.0) and (self.angle < 190.0)):
				return "W"
			if ((self.angle > 190.0) and (self.angle < 260.0)):
				return "SW"
			if ((self.angle > 260.0) and (self.angle < 280.0)):
				return "S"
			if ((self.angle > 280.0) and (self.angle < 350.0)):
				return "SE"
			if ((self.angle > 350.0) and (self.angle < 361)):
				return "E"
			else:
				return "None"
		if self.angle < 0:
			if ((self.angle < 0.0) and (self.angle > -10.0)):
				return "E"
			if ((self.angle < -10.0) and (self.angle > -80.0)):
				return "SE"
			if ((self.angle < -80.0) and (self.angle > -110.0)):
				return "S"
			if ((self.angle < -110.0) and (self.angle > -170.0)):
				return "SW"
			if ((self.angle < -170.0) and (self.angle > -190.0)):
				return "W"
			if ((self.angle < -190.0) and (self.angle > -260.0)):
				return "NW"
			if ((self.angle < -260.0) and (self.angle > -280.0)):
				return "N"
			if ((self.angle < -280.0) and (self.angle > -350.0)):
				return "NE"
			if ((self.angle < -350.0) and (self.angle > -361 )):
				return "E"
			else:
				return "None"
	def close(self):
		self.ser.close()
