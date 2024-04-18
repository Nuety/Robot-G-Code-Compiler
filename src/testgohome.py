import gcodehandler as gcr
import rtde_control
import rtde_receive
import re
import math

rotation = [0, 3.14, 0]

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")




rtde_c.moveJ([0,-3.14/2,0,-3.14/2,0,0], 2, 2)
rtde_c.moveJ([math.radians(13), math.radians(-120), math.radians(-103), math.radians(-45), math.radians(90), math.radians(0),], 2, 2)