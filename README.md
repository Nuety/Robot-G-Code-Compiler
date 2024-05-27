# Robot-G-Code-Compiler
## Calibrating
use the calibratebed.py file to mark the four corners of the hotbed, this will make the robot identify the height of each corner, these should be the same with +- 0.0001 (100 microns). to ensure the hotend will not go into the bed the heightoffset should be set to the average of the numbers when within the boundary (line 10 in controller.py). 

## running the printer
When the bed is calibrated select a gcode file to print by writing the name on line 28 in controller.py.