#!/usr/bin/env python

# Project: Person recognition, IKR
# Description: << popis >>
# Author: Radim Lipka, Tomas Scavincky
# Email: xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz
# Date: 29.4.2016
# File: << file name >>

__author__ = "Radim Lipka, Tomas Scavincky"
__version__ = "1.0"
__email__ = "xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz"
__date__ = "29.4.2016"

import re, getopt, wave, sys, os, re, struct, numpy as np


def main(args, argv):

# PARSING ARGUMENTS <-- TEST_FOLDER, INPUT_NET, OUTPUT_FILE

	test_input_data = list()
	results = str()

	if(args != 3):
		exit(1)

	try:
		# Testing data
		w_files_test = os.listdir(argv[0])
		if(argv[1].endswith("NET")):
			exit(2)
		w_file_output = open(argv[1], "w")
		net = nl.load(argv[2])

	except:
		exit(3)

# LOADING TESTING DATA

	print("\nLOADING TEST DATA\n")

	w_files_test = wav_to_mfcc(argv[0], w_files_test, test_input_data)

# TESTING

	print("\n\tTESTING with test data\n")

	for index in range(len(test_input_data)):
		score = net.sim([test_input_data[index]])[0][0]

		file_name = w_files_test[index].split('/')
		file_name = file_name[-1].split('.')
		file_name = file_name[-2]

		if(score > 0.5):
			decision = 1
		else:
		 	decision = 0

		print(file_name + " " + str(score) + " " + str(decision))
		results += file_name + " " + str(score) + " " + str(decision) + "\n"

	w_file_output.write(results)
	w_file_output.close()

	print("\nPROCESSED\n")

	return 0

if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
