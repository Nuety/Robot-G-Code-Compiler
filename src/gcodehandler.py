import re

class GCodeHandler:
    def __init__(self) -> None:
        pass

    def readfile(self, path):
        #open the file path here 
        cmd = []
        with open(path) as f:
            commands = f.read().splitlines()
            for i in commands:
                cmd.append(i.rstrip())

        return cmd
    
    def convertCode(self, commands):
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
                    path.append(["G28", 0, 0, 0, 0, 0])
                #Absolute Positioning
                case "G90":
                    pass
                #Relative Positioning
                case "G91":
                    pass
                #Set Position
                case "G92":
                    pass
                case "M104" | "M109" | "M140" | "M190":
                    path.append(self.extractTemperatures(i))
                
                case _:
                    pass
        return path

    def extractTemperatures(self, string):
        #extracts coordinates from command
        #extracts G0|G1 in [g,x,y,z,f,e]
        g = re.findall('([GM][\d.]+)', string)
        s = list(map(float, re.findall('S([\d.]+)', string)))

        tmp2 = [g, s]
        result = []

        for i in tmp2:
            if i:
                result.append(i[0])
            else:
                result.append(None)
        return result

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