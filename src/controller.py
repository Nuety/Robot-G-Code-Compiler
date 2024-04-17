import gcodereader as gcr
import rtde_control
import rtde_receive
import re
import math

#TODO save magic constants in seperate file


rotation = [0, 3.14, 0]

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

gcreader = gcr.reader()
commands = gcreader.readfile("20mm_cube.gcode")


class controller():
    def __init__(self) -> None:
        pass

    def returnHome(self):
        rtde_c.moveJ([0,-3.14/2,0,-3.14/2,0,0], 2, 2)
        rtde_c.moveJ([math.radians(13), math.radians(-120), math.radians(-103), math.radians(-45), math.radians(90), math.radians(0),], 2, 2)
                

    def extractCoordinates(self, string):
        #extracts coordinates from command
        #extracts G0|G1 in [g,x,y,z,f,e]
        g = re.findall('(G[\d.]+)', string)
        x = list(map(float, re.findall('X([\d.]+)', string)))
        y = list(map(float, re.findall('Y([\d.]+)', string)))
        z = list(map(float, re.findall('Z([\d.]+)', string)))
        f = list(map(float, re.findall('F([\d.]+)', string)))
        e = list(map(float, re.findall('E([\d.]+)', string)))

        tmp = [x, y, z]
        tmp2 = [g, None, None, None, f, e]
        result = []


        #TODO this is gross
        #TODO find a better way other than 3 lists and 2 forloops
        for i, coord in enumerate(tmp):
            if coord:
                #divide by 1000 since gcode uses mm values and we use meter
                tmp2[i+1] = [round(coord[0]/1000, 8)]

        for i in tmp2:
            if i:
                result.append(i[0])
            else:
                result.append(None)

        return result


    def convertCode(self, commands):
        #conta
        path = []
        for i in commands:
            #NOTE THAT I CHANGED THE NAME OF THE SPLITTED 'i'
            cmd = i.split()
            if not cmd:
                continue
            match cmd[0]:
                #move with or without extruder
                case "G0" | "G1":
                    #print(self.extractCoordinates(i))
                    path.append(self.extractCoordinates(i))
                #return home
                #TODO Check if filament stuff works with this method
                case "G28":
                    self.returnHome()
                #Absolute Positioning
                case "G90":
                    pass
                #Relative Positioning
                case "G91":
                    pass
                #Set Position
                case "G92":
                    pass
                case _:
                    pass
        return path
    
    def run(self, path):
        #the midpoint where the hotplate should sit is 0.46,0,0
        tot = len(path)
        height = 0.0
        speed = 0.015
        for i, segment in enumerate(path):
            print(f"{((i/tot)*100):.4f}% x: {segment[1]}, y: {segment[2]}, z: {height}")

            


            
            match segment[0]:
                #if it is either G0 or G1 make the move and 
                case "G0" | "G1":
                    #if height is set in the command change the command
                    if segment[3]:
                        height = segment[3]

                    #if speed is set change speed
                    if segment[4]:
                        #speed in gcode is mm/min and robot moves in m/s so we divide by 60000
                        speed = segment[4]/60000

                    #set extrution mode
                    if segment[0] == "G0":
                        #stop printing if G0
                        pass
                    else:
                        #start printing if G1
                        pass

                    #move the robotarm if both x and y exist
                    if segment[1] and segment[2]:
                        rtde_c.moveL([segment[1]+0.46, segment[2], height+0.1, rotation[0], rotation[1], rotation[2]], speed, 4)
                    


            



ctrl = controller()
path = ctrl.convertCode(commands)
ctrl.run(path)

