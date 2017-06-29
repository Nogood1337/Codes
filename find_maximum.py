#!/usr/bin/python
# -*- coding:utf-8 -*-
#standard python packages
import numpy as np
import math, time

##################################################
#changeable things

#outname = "text_files/" +  "maximum.txt"	#in case for saving
#namelist = ["BlueJet1_128GTU.txt", "BlueJet2_128GTU.txt", "BlueJet3_128GTU.txt", "BlueJet5_128GTU.txt", "BlueJet6_128GTU.txt", "BlueJet7_128GTU.txt", "Elves1_128GTU.txt", "Elves2_128GTU.txt", "Sprite1_128GTU.txt", "Sprite2_128GTU.txt", "Meteor_1_L2.txt", "Meteor_2_L2.txt"]	#in case of wanting to go through multiple files
want_time = 0	#0 for wanting to count execution time and print it in the terminal, anything else will not

#below is for testing
outname = "text_files/" +  "test_max.txt"
namelist = ["Meteor_1_L2.txt", "Meteor_2_L2.txt"]

##################################################

start = time.time()

maximimum_collection = []
for name in namelist:
	total_list = []	#list of every number in the file
	tempname = "text_files/" + name
	with open(tempname) as f:
		data = []
		for line in f:
			line = line.split()
			if line:
				line = [int(i) for i in line]
				data.append(line)	#making the text file into a list

		length = np.shape(data)[0]	#number of rows in the text file
		ind = range(0, length, 49)	#list of numbers with the indices in the list data indicating change in timestep, [0, 49, 98, 147....]
		nz = int(len(ind))	#nz is the total number of timesteps in the textfile
		counts = np.zeros((nz, 2304))	#list of nz lists each with 2304 zeros corresponding to each pixel
		for iz in range(nz):
			counts[iz][:] = np.concatenate((data[ind[iz] + 1 : ind[iz] + 49]), axis = 0)	#filling the nz lists with the data

	for maximum in counts:
		total_list.append(max(maximum))

	maximimum_collection.append(name + "  " + str(max(total_list)))


thefile = open(outname, 'w')
for line in maximimum_collection:	#goes through the total_list and writes each line in the text file
	thefile.write(line + "\n")

end = time.time()
if want_time == 0:
	print end-start

