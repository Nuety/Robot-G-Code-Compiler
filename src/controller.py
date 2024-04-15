import gcodereader as gcr
import rtde_control
import rtde_receive
import re

rotation = [0, 3.14, 0]

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

gcreader = gcr.reader()
commands = gcreader.readfile("20mm_cube.gcode")


class controller():
    def __init__(self) -> None:
        pass

    def extractCoordinates(self, string):
        #extracts coordinates from command
        #extracts G0|G1 in [x,y,z,f,e]
        x = list(map(float, re.findall('X([\d.]+)', string)))
        y = list(map(float, re.findall('Y([\d.]+)', string)))
        z = list(map(float, re.findall('Z([\d.]+)', string)))
        f = list(map(float, re.findall('F([\d.]+)', string)))
        e = list(map(float, re.findall('E([\d.]+)', string)))

        tmp = [x,y,z,f,e]
        result = []

        for i in tmp:
            if i:
                #divide by 1000 since gcode uses mm values and we use meter
                result.append(round(i[0]/1000, 8))
            else:
                result.append(None)
        return result
        

    def covertCode(self, commands):
        #conta
        trajectory = []
        for i in commands:
            #NOTE THAT I CHANGED THE NAME OF THE SPLITTED 'i'
            cmd = i.split()
            if not cmd:
                continue
            match cmd[0]:
                case "G0" | "G1":
                    #print(self.extractCoordinates(i))
                    trajectory.append(self.extractCoordinates(i))
                case "G28":
                    pass
                case "G90":
                    pass
                case "G91":
                    pass
                case "G92":
                    pass
                case _:
                    pass
        return trajectory
    
    def run(self, path):
        tot = len(path)
        height = 0.0
        for i, segment in enumerate(path):
            print(f"{(i/tot):.4f}% x: {segment[0]}, y: {segment[1]}, z: {height}")

            if segment[2]:
                height = segment[2]
                
            if segment[0] and segment[1]:
                rtde_c.moveL([segment[0]+0.46, segment[1], height+0.1, rotation[0], rotation[1], rotation[2]], 0.015, 2)



ctrl = controller()
path = ctrl.covertCode(commands)
ctrl.run(path)

