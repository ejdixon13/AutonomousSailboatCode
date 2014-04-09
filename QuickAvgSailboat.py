import time

from servo_control import PololuMicroMaestro
from windSensor import WindSensor

# This class initializes a wind sensor which is actually a temperature sensor hooked up to an analog to digital converter.
# It is also hooked up to a servo motor controller which does a sweep and compares the data agains four best fit lines stored as arrays of data
# named calculated_data. This way the data is defined once on startup and doesn't have to be generated for each sweep, saving processor time.
# There are several tests done in calcuateWindDirection that help to determine the direction. These have room for improvement, but for now,
# they are a good start to get a general idea of what can be done to characterize the wind directions.
class myWindSensor(object):
	def __init__ (self):
		# Initialize the analog to digital converter.
		self.wind_sensor = WindSensor()
		# Initialize the servo motor.
		self.robot = PololuMicroMaestro()
		# Startup and initialize the analog to digital converter phidget.
		self.wind_sensor.startup()
		# Initialize the angle of the servo motor that's plugged into port 2. The servo motor only really moves from about 50 degrees to
		# about 115 degrees, so doing more than that doesn't do a lot of good.
		self.robot.setAngle(2, 49)
		# averaged data from several samples of running the sweep
		self.calculated_data = [[0, 22.90789474, 40.16140351, 42.57368421, 45.35789474, 46.70263158, 47.6622807, 47.86403509, 48.04912281, 47.63421053, 46.61052632, 46.81315789, 46.04824561, 45.15526316, 45.63596491, 46.2754386, 45.63596491, 45.59824561, 44.76491228, 44.37192982, 43.57807018, 42.48508772, 41.71578947, 40.36754386, 39.70263158, 39.32017544, 38.60614035, 39.07192982, 39.24824561, 38.85964912, 37.60087719, 38.39649123, 38.70701754, 39.46052632, 38.29736842, 39.20789474, 38.72807018, 39.65350877, 39.81754386, 39.63859649, 39.61929825, 38.87631579, 37.88333333, 36.66403509, 35.44122807, 34.31754386, 31.98684211, 30.41754386, 27.67894737, 24.01491228, 21.71491228, 19.16140351, 16.76666667, 14.17719298, 11.73333333, 11.61754386, 10.46315789, 7.29122807, 5.907894737, 3.421929825, 2.372807018, 2.374561404, 1.93245614, 0.993859649, 0.28245614, 0.165789474], [0, 11.09298246, -11.51403509, -17.73947368, -22.19210526, -25.36929825, -26.41052632, -27.39736842, -30.60263158, -31.47017544, -33.07807018, -35.18947368, -35.97105263, -37.37719298, -36.88508772, -36.2754386, -35.98157895, -35.43245614, -35.75350877, -33.96929825, -32.98070175, -30.41929825, -26.19035088, -22.48070175, -22.30175439, -19.17894737, -14.79210526, -14.8622807, -15.71315789, -14.49473684, -5.653508772, -2.83245614, 0.549122807, 1.071929825, 1.234210526, 0.705263158, 3.96754386, 9.664912281, 8.55877193, 8.049122807, 11.0754386, 8.412280702, 9.313157895, 8.59122807, 9.466666667, 8.638596491, 10.09385965, 9.753508772, 9.250877193, 8.294736842, 8.764035088, 8.397368421, 6.600877193, 4.648245614, 1.785087719, 0.575438596, 2.754385965, 1.831578947, 0.235087719, -0.137719298, 0.522807018, -0.501754386, 0.444736842, 0.484210526, -0.311403509, -0.405263158], [0, -15.525, -5.1, 0.9, 5.45, 7.2, 6.95, 4.675, 4.3, 3.35, 2.1, 0.7, -1.95, -3.45, -5.9, -7.875, -8.675, -10.025, -10.65, -12.125, -13.4, -11.85, -11.85, -11.45, -13.475, -13.975, -12.875, -12.5, -14.15, -15, -15.575, -15.475, -16.175, -15.85, -15.575, -15.15, -15.95, -15.475, -16.6, -18.475, -19.225, -19.125, -19.05, -21.475, -23.05, -27.725, -27.75, -30.95, -29.375, -28.975, -27.825, -28.1, -29.2, -29.525, -26.9, -24.525, -21.725, -15.175, -11.525, -8.75, -7.1, -4.85, -3.45, -3.75, -2.925, -1.75], [0, -14.14561404, -18.41052632, -17.97719298, -16.79649123, -16.49385965, -16.04473684, -16.29035088, -16.36140351, -16.55701754, -16.06578947, -15.96403509, -15.42719298, -15.01929825, -15.81578947, -17.17017544, -17.20964912, -17.57807018, -18.07280702, -18.62807018, -19.45877193, -20.41403509, -21.29473684, -22.55263158, -23.87368421, -23.4754386, -24.60701754, -26.17105263, -27.29385965, -27.91578947, -28.62280702, -29.56842105, -30.39649123, -30.53157895, -31.19561404, -30.87719298, -31.01491228, -30.7122807, -31.18157895, -29.78508772, -29.1877193, -28.37894737, -27.34035088, -25.7877193, -24.44122807, -22.82894737, -21.6245614, -20.01666667, -18.19824561, -17.52105263, -15.82631579, -14.45789474, -12.2, -11.54561404, -10.2377193, -8.904385965, -7.483333333, -6.407894737, -5.5, -3.584210526, -3.026315789, -2.421929825, -1.378947368, -1.492105263, -1.398245614, -0.335087719]]
	# Calculate which direction the wind is coming from, store it in a queue and publish the majority of the queue to a file.
	# This is done so that the wind direction doesn't change too quickly by a random weird bit of data and throw the sailboat off.
	def calculateWindDirection(self):
		# Initial angle
		angle = 49
		# Initialize the temperatures array.
                temps = [1.0]
		# Initialize the directions
		directionQueue = [-1, -1, -1]
		# Total of all the data values
		total_all = 0
		# Do the servo sweep and gather all the data.
                while angle != 115:
                        angle += 1
                        self.robot.setAngle(2, angle)
			time.sleep(.1)
                        total = 0
			# Gather three data values at each angle and average them to get rid of random data values.
                        for index in range(0,3):
                                total += self.wind_sensor.getValue()
				# Sleep to give the data time to change.
                                time.sleep(.01)
			# Average out the data.
			avg = total/4
			# Add the current average to the temperatures array.
			temps.append(avg)
			# Add the current average to the total.
			total_all += (avg - temps[1])
		# Get rid of the initial dummy value used to initialize the temperatures array.
                temps.pop(0)
		first = temps[0]
		# Record both the absolute value and signed differences between the data gathered and the four best fit lines.
		signed_avg_diffs = [0, 0, 0, 0]
		avg_diffs = [0, 0, 0, 0]
		for indexa in range(0,len(avg_diffs)):
			total_diff = 0
			signed_total_diff = 0
			for indexb in range(0,114-50):
				signed_total_diff += (temps[indexb] - first) - self.calculated_data[indexa][indexb]
				total_diff += abs((temps[indexb] - first) - self.calculated_data[indexa][indexb])
			signed_avg_diffs[indexa] = signed_total_diff / 115
			avg_diffs[indexa] = total_diff / 115
		print "Signed avg diffs: "
		print signed_avg_diffs
		print "Abs avg diffs: "
		print avg_diffs
		# Possible directions are front, back, right, and left.
		directions = ["F", "B", "R", "L"]
		min_val = min(avg_diffs)
		# Initialize the direction to none.
		direction = "N"
		# Index in the directions array that is the current hypothesized direction.
		directionNum = -1
		# Find the minimum difference to give best guess as to the direction.
		for index in range(0,len(directions)):
			if avg_diffs[index] == min_val:
				directionNum = index
		# Do some other kind of random tests that seemed to help... :)
		if directionNum == 0:
			if (avg_diffs[0] > 30):
				min_bal = min(avg_diffs[1], avg_diffs[2], avg_diffs[3])
			for index in range(1, len(directions)):
				if avg_diffs[index] == min_val:
					directionNum = index
		if directionNum != 0 and avg_diffs[2] < avg_diffs[3]:
			directionNum = 3
		elif signed_avg_diffs[1] < 0 and signed_avg_diffs[2] < 0:
			directionNum = 1
		elif directionNum == 1:
			if avg_diffs[2] < avg_diffs[3]:
				directionNum = 3
			else:
				directionNum = 2
		elif directionNum == 0 and total_all < 0:
			if avg_diffs[2] < avg_diffs[3]:
                                directionNum = 3
                        else:
                                directionNum = 2
		elif directionNum == 2 or directionNum == 3:
			if signed_avg_diffs[1] <= avg_diffs[2] and signed_avg_diffs[1] <= avg_diffs[3]:
                                directionNum = 2
                        else:
                                directionNum = 3
		# Get the direction and display it to the current terminal.
		direction = directions[directionNum]
		print "Direction: " + direction
		# Add the direction to the queue and take off the oldest direction.
		directionQueue.append(directionNum)
		directionQueue.pop(0)
		counts = [0, 0, 0, 0]
		# Count the totals for each direction.
		for index in range(0, len(directionQueue)):
			if directionQueue[index] >= 0:
				counts[directionQueue[index]] += 1
		max = 0
		# Find the max count, and set the direction equal to that.
		for index in range(0, len(counts)):
			if (counts[index] > max):
				directionNum = index
		# Open the file to write to, write the direction, and close it right after so that the other program can access it.
		fo = open("wind.txt", "w+")
                fo.write(directions[directionNum])
                fo.close()

# Initialize the sensor and run it over and over.
myWindSensor = myWindSensor()
while True:
	myWindSensor.calculateWindDirection()


