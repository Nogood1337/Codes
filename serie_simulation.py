#!/usr/bin/python
# -*- coding:utf-8 -*-
#standard python packages
import numpy as np
import subprocess
import sys

#for now, this program is geared for changing the magnitude. to simulate for different parametres would need a little bit of tweaking, not hard though
start = 4	#the start magnitude
end = -5	#the end magnitude
number_of_sim = 3	#this may make the magnitudes into weird numbers, for example if start is 0 and end is 3 and 10 simulations is wanted then the magnitudes would be 0.0, 0.3333..., 0.6667... and so on. Since these numbers are theoretically possible this is not a problem to simulate.
sim_type = 1	#0 for meteors, anything else defaults to TLE simulations

if sim_type == 0:
	filename = "config/Generators/MeteorGenerator.cfg"
else:
	filename = "TLEGenerator.cfg"
list_to_change = np.linspace(start,end,number_of_sim)	#the list of all magnitudes to change between each simulation
for a in list_to_change:
	data = []
#	print a, sys.argv[0]
	with open(filename) as f:
#	with open("text_files/test.cfg") as f:
		for line in f:
			templine = line.split()
			if len(templine) != 0:
				if templine[0] == "TLEGenerator.absmag":
					line = "TLEGenerator.absmag      = " + str(a) + "    			#-0.9 #abs. mag of the TLE"
					print line
			data.append(line.strip())

	fil = open(filename, 'w')
#	fil = open("text_files/test.cfg", 'w')
	for line in data:
		fil.write(line + "\n")
	fil.close()

	#below is for sending the bash command
	if sim_type == 0:
		bashCommand = "./simulate_EVENTS_MiniEuso config/MiniEuso_v2METEOR.cfg"
	else:
		bashCommand = "./simulate_EVENTS_MiniEuso config/MiniEuso_v2TLE.cfg"
#	bashCommand = "python test.py"	#this is a test command to see how it worked
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)	#this makes process into the subprocess that excecuted the command
	output, error = process.communicate()

	print output.strip()


