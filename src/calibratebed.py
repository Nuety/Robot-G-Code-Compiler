import rtde_control
import rtde_receive
import time
rotation = [0, 3.14, 0]

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

#CCW DOWN
#CW UP

#brug d = 0.1
d = 0.1
x = 0.44
xoffset = 0
y = 0
yoffset = 0
z = 0.15
speed = 0.1
contactspeed = [0, 0, -0.01, 0, 0, 0]

#cable corner should be top left pointing towards the robot

rtde_c.moveL([x + d, y + d, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
bottomRightCorner = rtde_r.getActualTCPPose()[2]

rtde_c.moveL([x - d, y + d, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
topRightCorner = rtde_r.getActualTCPPose()[2]

rtde_c.moveL([x - d, y - d, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
topLeftCorner = rtde_r.getActualTCPPose()[2]

rtde_c.moveL([x + d, y - d, z, rotation[0], rotation[1], rotation[2]], speed, 4)
rtde_c.moveUntilContact(contactspeed)
bottomLeftCorner = rtde_r.getActualTCPPose()[2]

rtde_c.moveL([x + d, y - d, z, rotation[0], rotation[1], rotation[2]], speed, 4)

print(f"tl: {topLeftCorner}, tr: {topRightCorner}, bl: {bottomLeftCorner}, br: {bottomRightCorner}")