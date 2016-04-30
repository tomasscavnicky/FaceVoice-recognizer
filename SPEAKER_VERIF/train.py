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

from features import mfcc
from features import logfbank

from sound_library import wav_to_mfcc


import neurolab as nl

sampling = int(16000)
channels = int(1)


def main(args, argv):

# PARSING ARGUMENTS

	train_input_data=list()
	test_input_data=list()

	if(args != 4):
		exit(1)

	try:
		# Training data
		w_files_train	= os.listdir(argv[0])
		w_non_files_train = os.listdir(argv[1])
		# Testing data
		w_files_dev	= os.listdir(argv[2])
		w_non_files_dev	= os.listdir(argv[3])
	
	except:
		exit(2)

# LOADING TRAINING DATA

	print("LOADING TRAIN DATA")

	w_files_train = wav_to_mfcc(argv[0], w_files_train, train_input_data)

	train_output_data = [[1.0]] * len(train_input_data)
	
	w_non_files_train = wav_to_mfcc(argv[1], w_non_files_train, train_input_data)

	train_output_data = [[1.0]] * (len(train_input_data) - len(train_output_data))

# TRAINING NEURAL NETWORK

	print("\nTRAINING\n")

	minimal = float(train_input_data[0][0])
	maximal = float(minimal)

	for i in train_input_data:

		minimal = min(list([minimal, max(i)]))
		maximal = max(list([maximal, max(i)]))

	print("MINIMAL VALUE: " + str(minimal))
	print("MAXIMAL VALUE: " + str(maximal))

	print("SHAPE: " + str(len(train_input_data[0])))

	net = nl.net.newff([[minimal, maximal]] * len(train_input_data[0]), [26, 26, 1])

	# Train process
	er = net.train(np.asarray(train_input_data), np.asarray(train_output_data), show=1, goal=0.1)

# LOADING TESTING DATA

	print("\nLOADING TEST DATA\n")

	w_files_dev = wav_to_mfcc(argv[2], w_files_dev, test_input_data)

	test_output_data += [[0.0]] * (len(test_input_data)

	w_non_files_dev = wav_to_mfcc(argv[3], w_non_files_dev, test_input_data)

	test_output_data += [[0.0]] * (len(test_input_data) - len(test_output_data))

# TESTING

	print("\nTESTING\n")

	print("\n\tTESTING with train data\n")

	train_err = float(0.0)
	test_err = float(0.0)

	for index in range(len(train_input_data)):
		train = net.sim([train_input_data[index]])[0][0]
		error = round(abs(abs(train_output_data[index][0]) - abs(train)), 3)
		print("Excepted: " + str(train_output_data[index][0]) + "\tGot: " + str(round(train, 3)) + "\tError[%]: " + str(error * 100) + "\t\tFile: " + (w_files_train + w_non_files_train)[index])
		train_err += error

	print("\n\tTESTING with test data\n")

	for index in range(len(test_input_data)):
		train = net.sim([test_input_data[index]])[0][0]
		error = round(abs(abs(test_output_data[index][0]) - abs(train)), 3)
		print("Excepted: " + str(test_output_data[index][0]) + "\tGot: " + str(round(train, 3)) + "\tError[%]: " + str(error * 100) + "\t\tFile: " + (w_files_dev + w_non_files_dev)[index])
		test_err += error

	print("\nTESTED\n")

	print("\tTRAIN DATA RECONGNITION ERROR: " + str(round(train_err / len(w_files_train + w_non_files_train), 3)))
	print("\tTEST DATA  RECONGNITION ERROR: " + str(round(test_err / len(w_files_dev + w_non_files_dev), 3)))

	print("PROCESSED")

	return 0

# Pokud je soubor hlavni a je v nem main, jinak odstranit
if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
