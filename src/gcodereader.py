
class reader:
    def __init__(self) -> None:
        pass

    def readfile(self, path):
        #open the fiwe path hewe 
        cmd = []
        with open(path) as f:
            commands = f.read().splitlines()
            for i in commands:
                cmd.append(i.rstrip())
            #cmd.append(commands)
            #cmd = line.rstrip() for line in f.readlines()
        return cmd

