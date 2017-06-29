#!/usr/bin/python
# -*- coding:utf-8 -*-
#standard python packages
import numpy as np
import matplotlib.pyplot as plt
import math, time
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.animation import FuncAnimation


def update(q):	#function for the animation
	label = 'timestep {0}'.format(q+1)
	# Update the line and the axes (with a new xlabel). Return a tuple of
	# "artists" that have to be redrawn for this frame.
	temp = np.zeros((48, 48))
	rowchange = 0	#placeholder to see when to switch row
	row = 0	#placeholder for the current row
	for i in counts[q]:	#goes through each of the 2304 elements in counts[x] and makes a list of 48 elements, rows, each with 48 elements, columns
		temp[47-row][rowchange-row*48] = temp[47-row][rowchange-row*48]+i	#the "47-row" is inserting in opposite row since the y-axis is top to bottom by default which mean it needs to be inverted and that inverts the y-axis as well
		rowchange = rowchange+1
		if rowchange%48==0:	#when 48 numbers are done we switch to the next row
			row = row+1
	im = ax.matshow(temp)
	ax.set_title(label)
	ax.xaxis.set_ticks_position('bottom')	#by default in matshow() the x-axis is located at top and I prefer the bottom
	ax.invert_yaxis()	#the aforementioned invertion
	cax.cla()	#clear the color bar betweer each timestep
	plt.colorbar(im, cax=cax)
	return im, ax


if __name__ == '__main__':
	##################################################
	#changeable parameters

	timestamp = 3	#number between 0 and nz, have to run and see what nz is or check text file -----> label will be incremented once
	stampnr = 0	#0 for plotting sum of all timestamps, 1 for animated 1-48 any other number for plotting timestamp number "timestamp"
	interv = 150	#interval for changing frames in the animation in milliseconds
	savename = "plots/" + "test"	#this will be the name the plot or animation is saved as
	dots = 100	#dots per inch for the animation
	save_show = 2	#0 = only save plot, 1 = both save and show plot, any other number will just show the plot
	want_time = 0	#0 for wanting to count execution time and print it in the terminal, anything else will not

	##################################################

	start = time.time()

#	with open("text_files/Meteor_1_L3.txt") as f:
#	with open("text_files/Elves1_128GTU.txt") as f:
	with open("text_files/BlueJet1_128GTU.txt") as f:
#	with open("text_files/Sprite1_128GTU.txt") as f:
#	with open("text_files/test.txt") as f:
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

	fig = plt.figure()
	ax = plt.gca()
	divider = make_axes_locatable(ax)	#this is for the colorbar
	cax = divider.append_axes("right", size="5%", pad=0.1)
	temp = np.zeros((48, 48))	#making an array of zeros that is going to be filled with data
	if stampnr == 0:
		number = 0
		label = 'Plot of the sums of all timestamps'
		for a in counts:	#this will put all the timestamps in one plot
			rowchange = 0	#placeholder to see when to switch row
			row = 0	#placeholder for the current row
			for i in counts[number]:	#goes through each of the 2304 elements in counts[x] and makes a list of 48 elements, rows, each with 48 elements, columns
				temp[47-row][rowchange-row*48] = temp[47-row][rowchange-row*48]+i	#the "47-row" is inserting in opposite row since the y-axis is top to bottom by default which mean it needs to be inverted and that inverts the y-axis as well
				rowchange = rowchange+1
				if rowchange%48==0:	#when 48 numbers are done we switch to the next row
					row = row+1
			number = number+1
		im = ax.matshow(temp)
		ax.set_title(label)
		ax.xaxis.set_ticks_position('bottom')	#by default in matshow() the x-axis is located at top and I prefer the bottom
		ax.invert_yaxis()	#the aforementioned invertion
		plt.colorbar(im, cax=cax)
		if save_show == 0 or save_show == 1:
			fig.savefig(savename + ".eps")
	elif stampnr == 1:
		anim = FuncAnimation(fig, update, frames=np.arange(0, nz), interval=interv)
		if save_show == 0 or save_show == 1:
			anim.save(savename + ".gif", dpi=dots, writer="imagemagick")
	else:
		label = 'timestep {0}'.format(timestamp+1)
		rowchange = 0	#placeholder to see when to switch row
		row = 0	#placeholder for the current row
		for i in counts[timestamp]:	#goes through each of the 2304 elements in counts[x] and makes a list of 48 elements, rows, each with 48 elements, columns
			temp[47-row][rowchange-row*48] = i	#the "47-row" is inserting in opposite row since the y-axis is top to bottom by default which mean it needs to be inverted and that inverts the y-axis as well
			rowchange = rowchange+1
			if rowchange%48==0:	#when 48 numbers are done we switch to the next row
				row = row+1
		im = ax.matshow(temp)
		ax.set_title(label)
		ax.xaxis.set_ticks_position('bottom')	#by default in matshow() the x-axis is located at top and I prefer the bottom
		ax.invert_yaxis()	#the aforementioned invertion
		plt.colorbar(im, cax=cax)
		if save_show == 0 or save_show == 1:
			fig.savefig(savename + ".eps")

	end = time.time()
	if want_time == 0:
		print end-start

	if save_show != 0:
		plt.show()
