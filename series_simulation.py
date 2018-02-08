#!/usr/bin/python
# -*- coding:utf-8 -*-
#standard python packages
import numpy as np
import subprocess
import sys, glob, os, datetime

date = str(datetime.date.today())	#gets current date
time = str(datetime.datetime.now().strftime("%H:%M:%S:%f")[:-3])	#and current time down to milliseconds
new_dir_name = "simuout/" + date + "_" + time	#this will make a directory that is named after the date and time when this script was run
os.mkdir(new_dir_name)	#making of said directory within simuout

#############################################
#Changeable parameters
#for now, this program is geared for changing the magnitude which means to begin with the cfg file should have the other parameters set manually to what is sought after and then run this program. to simulate for different parametres would need a little bit of tweaking, not hard though
start = -1	#the start magnitude
end = -1	#the end magnitude, which should always be smaller than the start
increment = 1	#how large should each step be? for example with 0.5 between 0 and -2 we would get 0,-0.5,-1,-1.5 and -2
number_of_sim = 5	#number of simulations for each step, so for 3 between 1 and -1 with 1 as increment we would get 1,1,1,0,0,0,-1,-1,-1
sim_type = 1	#0 for meteors, anything else defaults to TLE simulations
#############################################

if sim_type == 0:
	filename = "config/Generators/MeteorGenerator.cfg"
else:
	filename = "config/Generators/TLEGenerator.cfg"
#before the actual simulations the following is so that one can know what were done in the simulations
changename = 'changes_between_sims.txt'
subprocess.check_call('cp ' + filename + ' ' + new_dir_name, shell=True)	#this copies the config that is used as a base for the series simulations
fil = open(new_dir_name + '/' + changename, 'w')
fil.write('This file contains the changeable parameters in the series_simulation.py that was used for all the simulations in this directory' + "\n")
fil.write('start: ' + str(start) + "\n")
fil.write('end: ' + str(end) + "\n")
fil.write('increment: ' + str(increment) + "\n")
fil.write('number_of_sim: ' + str(number_of_sim) + "\n")
fil.write('sim_type: ' + str(sim_type) + '    #This is not the same type as in the config, this is just 0 for meteors and 1 for the rest')
fil.close()

#the following is to get the list of the magnitudes to loop through
total_number_of_sim = (((start-end)/increment)+1)*number_of_sim	#we must have +1 to include the 0 magnitude
count = start
list_to_change = []
while count >= end:
	temp_count = 0
	while temp_count < number_of_sim:
		list_to_change.append(count)
		temp_count = temp_count + 1
	count = count - increment
list_to_change = np.asarray(list_to_change)


for a in list_to_change:
	times = 0
	while times < number_of_sim:	#this will run the same magnitude as many times as number_of_sim is required to be
		data = []
		with open(filename) as f:
			for line in f:
				templine = line.split()
				if len(templine) != 0:
					if templine[0] == "TLEGenerator.absmag":
						line = "TLEGenerator.absmag      = " + str(a) + "    			#-0.9 #abs. mag of the TLE"
						print line
				data.append(line.strip())

		fil = open(filename, 'w')
		for line in data:
			fil.write(line + "\n")
		fil.close()


		#below is for sending the bash command
		if sim_type == 0:
			bashCommand = "./simulate_EVENTS_MiniEuso config/MiniEuso_v2METEOR.cfg"
		else:
			bashCommand = "./simulate_EVENTS_MiniEuso config/MiniEuso_v2TLE.cfg"
		subprocess.check_call(bashCommand, shell=True)	#as long as the command is not user inputed the shell=True is ok, otherwise shell injection = problems


		#below is for the handling of the root files created during each loop
		list_of_files = glob.glob('output/*.root')	#this will find all root files within output where each simulation is stored
		latest_file = max(list_of_files, key=os.path.getctime)	#this finds the latest created root file
		os.rename(latest_file, new_dir_name + "/" + latest_file.strip("output/") + "t")	#and this moves the latest root file to the directory created in the beginning, the extra t is ugly since i don't know why but the strip("output/") removes the last t in .txt for some reason
		times = times+1

print "SCRIPT IS DONE"	#in case everything worked as it should this will be shown
