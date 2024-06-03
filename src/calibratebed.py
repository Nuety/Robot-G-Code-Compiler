import rtde_control
import rtde_receive
import time
rotation = [0, 3.14, 0]

#Init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

#Calibrate bed height by turning screwhandles
#CCW DOWN
#CW UP

#The distance d is used to move hotend to the four corners
#d is half the length of the bed sides
d = 0.09

x = 0.46
xoffset = -0.05

y = 0
yoffset = 0.0

z = 0.15

speed = 0.1
contactspeed = [0, 0, -0.01, 0, 0, 0]

#Cable corner should be top left pointing towards the robot
#Move to each corner and get the z value
rtde_c.moveL([x + d + xoffset, y + d + yoffset, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
bottomRightCorner = rtde_r.getActualTCPPose()[2]
time.sleep(0.05)

rtde_c.moveL([x - d + xoffset, y + d + yoffset, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
topRightCorner = rtde_r.getActualTCPPose()[2]
time.sleep(0.05)

rtde_c.moveL([x - d + xoffset, y - d + yoffset, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
topLeftCorner = rtde_r.getActualTCPPose()[2]
time.sleep(0.05)

rtde_c.moveL([x + d + xoffset, y - d + yoffset, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
bottomLeftCorner = rtde_r.getActualTCPPose()[2]
time.sleep(0.05)

rtde_c.moveL([x + d + xoffset, y - d + yoffset, z, rotation[0], rotation[1], rotation[2]], speed, 4)
#Print out the height of each corners - becoming the height offset of the controller
print(f"tl: {topLeftCorner}, tr: {topRightCorner}, bl: {bottomLeftCorner}, br: {bottomRightCorner}")