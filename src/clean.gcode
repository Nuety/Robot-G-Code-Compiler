;FLAVOR:Marlin
;TIME:3243
;Filament used: 1.67787m
;Layer height: 0.2
;MINX:96.064
;MINY:87.066
;MINZ:0.2
;MAXX:123.94
;MAXY:132.909
;MAXZ:37.4
;TARGET_MACHINE.NAME:Creality Ender-3 Pro
;Generated with Cura_SteamEngine 5.6.0
M82 ;absolute extrusion mode
; Ender 3 Custom Start G-code
G92 E0 ; Reset Extruder
G28 ; Home all axes
G1 Z5.0 F3000 ; Move Z Axis up a bit during heating to not damage bed
M104 S175 ; Start heating up the nozzle most of the way
M190 S60 ; Start heating the bed, wait until target temperature reached
M109 S200 ; Finish heating the nozzle
G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed
G1 X0.1 Y20 Z0.3 F5000.0 ; Move to start position
G1 X0.1 Y200.0 Z0.3 F1500.0 E15 ; Draw the first line
G1 X0.4 Y200.0 Z0.3 F5000.0 ; Move to side a little
G1 X0.4 Y20 Z0.3 F1500.0 E30 ; Draw the second line
G92 E0 ; Reset Extruder
G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed
G1 X5 Y20 Z0.3 F5000.0 ; Move over to prevent blob squish
G92 E0
G92 E0
G1 F1500 E-6.5
;LAYER_COUNT:187
;LAYER:0
M107
G0 F6000 X100.24 Y96.989 Z0.2
;TYPE:SKIRT



G91 ;Relative positioning
G1 E-2 F2700 ;Retract a bit
G1 E-2 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z10 ;Raise Z more
G90 ;Absolute positioning

G1 X0 Y220 ;Present print
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z

M82 ;absolute extrusion mode
M104 S0
;End of Gcode
;SETTING_3 {"global_quality": "[general]\\nversion = 4\\nname = Standard Quality
;SETTING_3  #2\\ndefinition = creality_ender3pro\\n\\n[metadata]\\ntype = qualit
;SETTING_3 y_changes\\nquality_type = standard\\nsetting_version = 22\\n\\n[valu
;SETTING_3 es]\\nadhesion_type = brim\\n\\n", "extruder_quality": ["[general]\\n
;SETTING_3 version = 4\\nname = Standard Quality #2\\ndefinition = creality_ende
;SETTING_3 r3pro\\n\\n[metadata]\\ntype = quality_changes\\nquality_type = stand
;SETTING_3 ard\\nsetting_version = 22\\nposition = 0\\n\\n[values]\\ninfill_spar
;SETTING_3 se_density = 20\\n\\n"]}
