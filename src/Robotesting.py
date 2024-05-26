import rtde_control
import rtde_receive

rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")
tmp = [[0.416, -0.107, 0.10, 0, 3.14, 0], [0.406, -0.107, 0.10, 0, 3.14, 0], [0.406, -0.117, 0.10, 0, 3.14, 0],[0.416, -0.117, 0.10, 0, 3.14, 0]]

for i in tmp:
  rtde_c.moveL(i, 0.05, 4)
for i in tmp:
  rtde_c.moveL(i, 0.05, 3)
for i in tmp:
  rtde_c.moveL(i, 0.05, 2)
for i in tmp:
  rtde_c.moveL(i, 0.05, 1)
for i in tmp:
  rtde_c.moveL(i, 0.05, 0.5)
rtde_c.stopScript()