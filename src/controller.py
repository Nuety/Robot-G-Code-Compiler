import gcodehandler as gch
import rtde_control
import rtde_receive
import re
import math

#TODO save magic constants in seperate file

rotation = [0, 3.14, 0]

#init robot connection
rtde_c = rtde_control.RTDEControlInterface("192.168.3.102")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.3.102")

GCHandler = gch.GCodeHandler()
commands = GCHandler.readfile("20mm_cube.gcode")


class controller():
    def __init__(self) -> None:
        self.relative = False
        pass



    def returnHome(self):
        rtde_c.moveJ([math.radians(13), math.radians(-120), math.radians(-103), math.radians(-45), math.radians(90), math.radians(90),], 2, 2)
                
    
    def run(self, path):
        #the midpoint where the hotplate should sit is 0.46,0,0
        #tot is to calculate a simple percentage meter
        tot = len(path)
        height = 0.0
        speed = 0.015
        for i, segment in enumerate(path):
            
            match segment[0]:
                #if it is either G0 or G1 make the move and 
                case "G0" | "G1":
                    print(f"{((i/tot)*100):.4f}% x: {segment[1]}, y: {segment[2]}, z: {height}")
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

                    match self.relative:
                        case True:
                            pass
                        
                        case False:
                            #move the robotarm if both x and y exist
                            if segment[1] and segment[2]:
                                rtde_c.moveL([segment[1]+0.46, segment[2], height+0.1, rotation[0], rotation[1], rotation[2]], speed, 4)
                    
                case "G28":
                    self.returnHome()

                #Absolute Positioning
                case "G90":
                    self.relative = False
                #Relative Positioning
                case "G91":
                    self.relative = True


            



ctrl = controller()
path = GCHandler.convertCode(commands)
ctrl.run(path)

