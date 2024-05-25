import rtde_control
import rtde_receive
import math

rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

tmp = [[0.416, -0.107, 0.10, 0, 3.14, 0], [0.406, -0.107, 0.10, 0, 3.14, 0], [0.406, -0.117, 0.10, 0, 3.14, 0],[0.416, -0.117, 0.10, 0, 3.14, 0]]

for i in tmp:
  rtde_c.moveL(i, 0.005, 4)

for i in tmp:
  rtde_c.moveL(i, 0.005, 3)

for i in tmp:
  rtde_c.moveL(i, 0.005, 2)

for i in tmp:
  rtde_c.moveL(i, 0.005, 1)

rtde_c.stopScript()