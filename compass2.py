import math
import time
from i2clibraries import i2c_hmc5883l
 
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
 
# closest to 8 cardinal direction values
xVals = [17, 131, 156, 107, -75, -200, -208, -154]
yVals = [-265, -168, -24, 87, 144, 69, -81, -215]
hmc5883l.setContinuousMode()
hmc5883l.setDeclination(9,54)

while True:
    t = hmc5883l.getAxes() # return compass data
    x = t[0] # get x coordinate data from compass
    y = t[1] # get y coordinate data from compass

    # initial compass positioning
    curDiff = 2000
    direction = 9
    try:
        for index in range(len(xVals)):
            # represents the values grabbed from the compass and the 
            # difference represents which x and y values the compass 
            # data is closest to
            totalDiff = abs(x - xVals[index]) + abs(y - yVals[index])
            if totalDiff < curDiff:
                direction = index # cardinal direction asscoiation
                curDiff = totalDiff # new compass direction
    except valueError:
        print("Direction failed")
    fo = open("direction.txt", "w+")
    if direction == 0:
        fo.write('NO')
        print('NORTH')
    elif direction == 1:
        fo.write('NE')
        print('NE')
    elif direction == 2:
        fo.write('EA')
        print('EAST')
    elif direction == 3:
        fo.write('SE')
        print('SE')
    elif direction == 4:
        fo.write('SO')
        print('SOUTH')
    elif direction == 5:
        fo.write('SW')
        print('SW')
    elif direction == 6:
        fo.write('WE')
        print('West')
    elif direction == 7:
        fo.write('NW')
        print('NW')
    else:
        fo.write('Z')
        print('Z')
    fo.close();
    time.sleep(1)

print(hmc5883l.getAxes())
