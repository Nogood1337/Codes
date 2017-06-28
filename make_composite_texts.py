#!/usr/bin/python
# -*- coding:utf-8 -*-
#standard python packages

##################################################
#changeable things

#outname = "text_files/" +  "Total_1.txt"	#name of the output text file, REMEMBER TO CHANGE OR IT WILL OVERWRITE
#namelist = ["JustBackground_128GTU.txt", "Sprite1_128GTU.txt", "JustBackground_128GTU.txt", "Elves1_128GTU.txt", "JustBackground_128GTU.txt", "BlueJet1_128GTU.txt", "JustBackground_128GTU.txt", "Meteor_1_L2.txt", "JustBackground_128GTU.txt"]	#list the names of all text files that you want to put into one large file making sure you have "JustBackground_128GTU.txt" before and after each filename. format it like this example: ["JustBackground_128GTU.txt", "name1.txt", "JustBackground_128GTU.txt", "name2.txt", "JustBackground_128GTU.txt", "name3.txt", "JustBackground_128GTU.txt"]

#below is for testing
outname = "text_files/" +  "test.txt"
namelist = ["Meteor_1_L3.txt", "Elves1_128GTU.txt"]

##################################################


total_list = []	#this will be the list to write to the text file
for name in namelist:	#loop through all the text files
	tempname = "text_files/" + name
	with open(tempname) as filename:	#open current text file in the loop
		for row in filename:
			total_list.append(row)	#adding each row to the total_list

thefile = open(outname, 'w')
for line in total_list:	#goes through the total_list and writes each line in the text file
	thefile.write(line)

