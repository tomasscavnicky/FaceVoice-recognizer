#!/usr/bin/env python

# Project: Person recognition, IKR
# Description: Z vysledku obou klasifikatoru sestavi dalsi klasifikaci na zaklade jejich vyhodnoceni
# Author: Radim Lipka, Tomas Scavincky
# Email: xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz
# Date: 29.4.2016
# File: speech_image.py

__author__ = "Radim Lipka, Tomas Scavincky"
__version__ = "1.0"
__email__ = "xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz"
__date__ = "29.4.2016"

import sys, os, numpy as np

# Input arguments: Speech_log_file, Image_log_file, Output_log_file

def main(args, argv):

	if(args != 3):
		exit(1)

	try: 
		speech_file = open(argv[0], "r")
		image_file = open(argv[1], "r")
		speech_image_file = open(argv[2], "w")
	except:
		exit(5)

	speech_data = sorted(speech_file.readlines(), key=lambda result: result[0])
	image_data = sorted(image_file.readlines(), key=lambda result: result[0])

	for dato in range(len(speech_data)):
		speech_data[dato] = speech_data[dato].split(' ')

	for dato in range(len(image_data)):
		image_data[dato] = image_data[dato].split(' ')

	for dato in range(len(speech_data) if (len(speech_data) == len(image_data)) else 0):
		if(image_data[dato][0] != speech_data[dato][0]):
			exit(6)

	SI_agree = int(0)
	SI_disagree = int(0)

	for index in range(len(speech_data)):
		mixed_score = (float(speech_data[index][1]) + float(image_data[index][1])) / 2
		hard_score = 1 if(mixed_score > 0.5) else 0

		print("FILE:  " + speech_data[index][0] + "\tSCORE:  " + str(round(mixed_score, 3)) + "\t\tHARD_DECISION:  " + str(hard_score))
		speech_image_file.write(speech_data[index][0] + " " + str(mixed_score) + " " + str(hard_score) + "\n")

		SI_agree += 1 if(speech_data[index][2] == image_data[index][2]) else 0
		SI_disagree += 1 if(speech_data[index][2] != image_data[index][2]) else 0

	print("\nRESULTS\n")
	print("Same results with botw clasiffiers:      " + str(SI_agree))
	print("Different result with botw claffiers: " + str(SI_disagree))

	print("\nFINISHED\n")

if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])






# End of file speech_image.py
