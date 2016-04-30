#!/usr/bin/env python

# Project: Person recognition, IKR
# Description: Trenovani neuronove site vyuzite pro klasifikaci
# Author: Radim Lipka, Tomas Scavincky
# Email: xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz
# Date: 29.4.2016
# File: train.py

__author__ = "Radim Lipka, Tomas Scavincky"
__version__ = "1.0"
__email__ = "xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz"
__date__ = "29.4.2016"

import re, getopt, wave, sys, os, re, struct, numpy as np

from features import mfcc
from features import logfbank

from base import wav_to_mfcc

import matplotlib.pyplot as plt
import neurolab as nl


	
sampling = int(16000)
channels = int(1)

def main(args, argv):

# PARSING ARGUMENTS

	train_input_data=list()
	test_input_data=list()

	if(args != 5):
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
	train_output_data = [[1.0]] * len(w_files_train)
	
	w_non_files_train = wav_to_mfcc(argv[1], w_non_files_train, train_input_data)
	train_output_data += [[0.0]] * (len(train_input_data) - len(train_output_data))

# PLOTTING FEATURES

	plt.figure(figsize=(20, 10), dpi=80)
	plt.ylim(-30.0, 30.0)
	plt.xlim(-1.0, (len(train_input_data[0]) + 1))
	plt.subplot(1, 1, 1)

	for index1 in range(len(train_input_data)):

		for index2 in range(len(train_input_data[index1])):
			if(train_output_data[index1] == [1.0]):
				plt.scatter(index2, train_input_data[index1][index2], color='blue')
			else:
				plt.scatter((index2 + 0.2), train_input_data[index1][index2], color='red')

	plt.show()

# TRAINING NEURAL NETWORK

	print("\nTRAINING\n")

	minimal = float(train_input_data[0][0])
	maximal = float(minimal)

	for i in train_input_data:

		minimal = min(list([minimal, min(i)]))
		maximal = max(list([maximal, max(i)]))

	print("MINIMAL VALUE: " + str(minimal))
	print("MAXIMAL VALUE: " + str(maximal))

	print("SHAPE: " + str(len(train_input_data[0])))

	net = nl.net.newff([[minimal, maximal]] * len(train_input_data[0]), [13, 13, 1])

	# Train process
	er = net.train(np.asarray(train_input_data), np.asarray(train_output_data), show=1, goal=0.05)

# LOADING TESTING DATA

	print("\nLOADING TEST DATA\n")

	w_files_dev = wav_to_mfcc(argv[2], w_files_dev, test_input_data)
	test_output_data = [[1.0]] * (len(w_files_dev))

	w_non_files_dev = wav_to_mfcc(argv[3], w_non_files_dev, test_input_data)
	test_output_data += [[0.0]] * (len(test_input_data) - len(test_output_data))

# TESTING

	print("\nTESTING\n")

	print("\n\tTESTING with train data\n")

	train_err = float(0.0)
	test_err = float(0.0)

	Correct_data_OK = int(0)
	Correct_data_FAIL = int(0)
	InCorrect_data_OK = int(0)
	InCorrect_data_FAIL = int(0)

	for index in range(len(train_input_data)):
		train = net.sim([train_input_data[index]])[0][0]
		error = round(abs(train_output_data[index][0] - train), 3)
		print("Excepted: " + str(train_output_data[index][0]) + "\tGot: " + str(round(train, 3)) + "\tError[%]: " + str(error * 100) + "\t\tFile: " + (w_files_train + w_non_files_train)[index])
		train_err += error

	print("\n\tTESTING with test data\n")

	for index in range(len(test_input_data)):
		train = net.sim([test_input_data[index]])[0][0]
		error = round(abs(test_output_data[index][0] - train), 3)
		print("Excepted: " + str(test_output_data[index][0]) + "\tGot: " + str(round(train, 3)) + "\tError[%]: " + str(error * 100) + "\t\tFile: " + (w_files_dev + w_non_files_dev)[index])
		test_err += error

		if(test_output_data[index][0] == 1 and error < 0.5):
			Correct_data_OK += 1
		elif(test_output_data[index][0] == 1 and error >= 0.5):
			Correct_data_FAIL += 1
		elif(test_output_data[index][0] == 0 and error < 0.5):
			InCorrect_data_OK += 1
		else:
		 	InCorrect_data_FAIL += 1

	print("\nTESTED\n")

	print("\tTRAIN DATA RECONGNITION ERROR: " + str(round(train_err / len(w_files_train + w_non_files_train), 3)))
	print("\tTEST DATA  RECONGNITION ERROR: " + str(round(test_err / len(w_files_dev + w_non_files_dev), 3)))

	print("\nTEST DATA STATISTICS:\n")
	print("\tCorrect data Recognized          [OK]:     " + str(Correct_data_OK))
	print("\tCorrect data not Recognized    [FAIL]:     " + str(Correct_data_FAIL))
	print("\tInCorrect data Recognized        [OK]:     " + str(InCorrect_data_OK))
	print("\tInCorrect data not Recognized  [FAIL]:     " + str(InCorrect_data_FAIL))

	print("\tOK:   " + str(Correct_data_OK + InCorrect_data_OK))
	print("\tFAIL:  " + str(Correct_data_FAIL + InCorrect_data_FAIL))

	try:
		print(str(argv[4] + "/" + str(argv[5]) + str(Correct_data_FAIL + InCorrect_data_FAIL) + str("_NET")))
		net.save(str(argv[4] + "/" + str(argv[5]) + str(Correct_data_FAIL + InCorrect_data_FAIL) + str("_NET")))
	except:
		print("\nERROR: Saving net\n")

	print("\nPROCESSED\n")

	return 0

if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file train.py
