import re

class GCodeHandler:
    def __init__(self) -> None:
        pass

    def readfile(self, path):
        #Open the file path here 
        cmd = []
        with open(path) as f:
            commands = f.read().splitlines()
            for i in commands:
                cmd.append(i.rstrip())
        #return list of lists
        return cmd
   
    def convertCode(self, commands):
        path = []
        for i in commands:
            cmd = i.split()
            if not cmd:
                continue
            match cmd[0]:
                #Move with or without extrusion
                case "G0" | "G1":
                    path.append(self.extractCoordinates(i))
                #Return home
                case "G28":
                    path.append(["G28", 0, 0, 0, 0, 0])
                #Absolute Positioning
                case "G90":
                    path.append(["G90", 0, 0, 0, 0, 0])
                #Relative Positioning
                case "G91":
                    path.append(["G91", 0, 0, 0, 0, 0])
                #Set Position
                case "G92":
                    pass
                case "M104" | "M109" | "M140" | "M190":
                    path.append(self.extractTemperatures(i))
                case _:
                    pass
        return path

    def extractTemperatures(self, string):
        #Extracts parameter from command
        #Find G or M followed by some number
        cmd = re.findall('([GM][\d.]+)', string)
        s = list(map(float, re.findall('S([\d.]+)', string)))

        tmp = [cmd, s]
        result = []

        for i in tmp:
            if i:
                result.append(i[0])
            else:
                result.append(None)
        return result

    def extractCoordinates(self, string):
        #Extracts coordinates from command
        #Extracts G0|G1 in [cmd,x,y,z,f,e]
        cmd = re.findall('(G[\d.]+)', string)
        x = list(map(float, re.findall('X([\d.]+)', string)))
        y = list(map(float, re.findall('Y([\d.]+)', string)))
        z = list(map(float, re.findall('Z([\d.]+)', string)))
        f = list(map(float, re.findall('F([\d.]+)', string)))
        e = list(map(float, re.findall('E([\d.]+)', string)))

        tmp = [x, y, z]
        tmp2 = [cmd, None, None, None, f, e]
        result = []

        for i, coord in enumerate(tmp):
            if coord:
                #Divide by 1000 since gcode uses mm values and we use meter
                tmp2[i+1] = [round(coord[0]/1000, 8)]
        for i in tmp2:
            if i:
                result.append(i[0])
            else:
                result.append(None)
        return result