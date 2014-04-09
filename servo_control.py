import serial
import time

# this class represents the specific servo controller that we used and
# it's functions
class PololuMicroMaestro(object):
    def __init__(self, port= "/dev/ttyACM0"):
        self.ser = serial.Serial(port = port) 
        self.angle = 0
    ## allows you to set angle of servo and which servo channel to use
    def setAngle(self, channel, angle):
        minAngle = 0.0
        maxAngle = 180.0
        minTarget = 256.0
        maxTarget = 13120.0
        scaledValue = int((angle / ((maxAngle - minAngle) / (maxTarget - minTarget))) + minTarget)

        # create command by setting proper bits
        commandByte = chr(0x84)
        channelByte = chr(channel)
        lowTargetByte = chr(scaledValue & 0x7F)
        highTargetByte  = chr((scaledValue >> 7) & 0x7F)
        command = commandByte + channelByte + lowTargetByte + highTargetByte
        
        # sends command to proper servo
        self.ser.write(command)
        self.angle = angle
        self.ser.flush()
    def close(self):
        self.ser.close()
    def getAngle(self):
        return self.angle

# Test main to give you an idea how the servos work
if __name__=="__main__":
    robot = PololuMicroMaestro()
    angle = 0
    while angle != 180:
        angle = input("Angle: ")
        robot.setAngle(0, angle)
        robot.setAngle(1, angle)
        robot.setAngle(2, angle)
        robot.setAngle(3, angle)
        robot.setAngle(4, angle)
        robot.setAngle(5, angle)

