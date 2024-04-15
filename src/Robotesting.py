import rtde_control
import rtde_receive
import math

rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")
home = [0.406, -0.107, 0.10, 0, 3.14, 0]

rtde_c.moveL(home, 0.2, 1)
tmp = [[0.406, -0.107, 0.10, 0, 3.14, 0], [0.407, -0.107, 0.10, 0, 3.14, 0], [0.407, -0.108, 0.10, 0, 3.14, 0],[0.406, -0.108, 0.10, 0, 3.14, 0]]
#[[G1, F1000, X0.01, Y0.01, E0.0], [G01, X2, Y2, E0.1], [G0, F9000, X3, Y3], [G0, X0, Y0]] 
#path_pose1 = [-0.143, -0.435, 0.20, -0.001, 3.12, 0.04, velocity, acceleration, blend_1]
#path_pose2 = [-0.143, -0.51, 0.21, -0.001, 3.12, 0.04, velocity, acceleration, blend_2]
#path_pose3 = [-0.32, -0.61, 0.31, -0.001, 3.12, 0.04, velocity, acceleration, blend_3]
#tmp = [[0.50, -0.17, 0.10, 0, 3.14, 0, 0.01, 0.3, 0], [0.50, -0.18, 0.10, 0, 3.14, 0, 0.01, 0.3, 0],[0.46, -0.18, 0.10, 0, 3.14, 0, 0.01, 0.3, 0]]
#rtde_c.moveL(tmp)
while(True):
  for i in tmp:
    rtde_c.moveL(i, 0.005, 2)

# rtde_c.moveL([0.46, 0.34, 0.10, 0, 3.14, 0], 0.05, 0.3)
# rtde_c.moveL([0.80, 0.34, 0.10, 0, 3.14, 0], 0.7, 0.3)
# rtde_c.moveL([0.80, 0.0, 0.10, 0, 3.14, 0], 0.7, 0.3)
# rtde_c.moveL([0.80, -0.34, 0.10, 0, 3.14, 0], 0.7, 0.3)
# rtde_c.moveL([0.46, -0.34, 0.10, 0, 3.14, 0], 0.7, 0.3)
# rtde_c.moveL([0.46, -0.0, 0.10, 0, 3.14, 0], 0.7, 0.3)
#rtde_c.moveL([0.80, -0.0, 0.10, 0, 3.14, 0], 1, 0.3)

rtde_c.stopScript()