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

import neurolab as nl

#import neurolab as nl

sampling = 16000

def short_to_mfcc(signal):

	global sampling

	mfcc_features = mfcc(signal, samplerate=sampling, winlen=0.025, winstep=0.01, numcep=13, nfilt=26, nfft=512, lowfreq=0, highfreq=1000, preemph=0.97, ceplifter=22, appendEnergy=True)
	fbank_features = logfbank(signal, sampling)

	#print(fbank_features[1:3,:])

	#return fbank_features[1:3,:]
	return fbank_features[1:2,:]

def wav_to_short(wave_file):

	global sampling

	# Library wave 
	w = wave.open(wave_file)

	# Starting from 1. sec because of booms
	if(sampling >= w.getnframes()):
		return

	length = w.getnframes() - sampling

	w.setpos(sampling)
	wav_samples = w.readframes(length)

	# Library struct 
	short_samples = struct.unpack("%ih" % (length* w.getnchannels()), wav_samples)
	return np.asarray(short_samples)

def wav_to_mfcc(path, w_files, mfcc_output):

	files = list()

	for w_file in sorted(w_files):

		if not (w_file.endswith(".wav")):
			continue

		print("Processing: " + w_file)
		content = wav_to_short(path + w_file)
		files.append(path + w_file)

		mfcc_output.append(short_to_mfcc(content).tolist()[0])
	
	w_files = files

def main(args, argv):

	train_input_data=list()
	test_input_data=list()

	if(args != 4):
		exit(1)

	try:
		w_files_train	= os.listdir(argv[0])
		w_files_dev	= os.listdir(argv[1])
		w_non_files_train = os.listdir(argv[2])
		w_non_files_dev	= os.listdir(argv[3])
	
	except:
		exit(2)

	print("LOADING TRAIN DATA")

	wav_to_mfcc(argv[0], w_files_train, train_input_data)

	train_output_data = [[1.0]] * len(train_input_data)

	wav_to_mfcc(argv[1], w_files_dev, train_input_data)

	train_output_data += [[0.0]] * (len(train_input_data) - len(train_output_data))

	print("LOADING TEST DATA")

	wav_to_mfcc(argv[2], w_non_files_train, test_input_data)

	test_output_data = [[1.0]] * len(test_input_data)

	wav_to_mfcc(argv[3], w_non_files_dev, test_input_data)

	test_output_data += [[0.0]] * (len(test_input_data) - len(test_output_data))
	
	print("TRAINING")

	minimal = float(0)
	maximal = float(0)

	for i in train_input_data:

		minimal = min(list([minimal, max(i)]))
		maximal = max(list([maximal, max(i)]))

	print("MINIMAL VALUE: " + str(minimal))
	print("MAXIMAL VALUE: " + str(maximal))

	print("SHAPE: " + str(len(train_input_data[0])))

	#net = nl.net.newff([[minimal, maximal]] * len(train_input_data[0]), [26, 26, 1])
	net = nl.net.newff([[minimal, maximal]] * len(train_input_data[0]), [26, 1])

	# Train process
	err = net.train(np.asarray(train_input_data), np.asarray(train_output_data), show=10, goal=1.0)

	print("TESTING with train data")

	train_err = float(0.0)
	test_err = float(0.0)

	for index in range(len(train_input_data)):
		train = net.sim([train_input_data[index]])[0][0]
		error = round(abs(abs(train) - abs(train_output_data[index][0])), 3)
		print("Excepted: " + str(train_output_data[index][0]) + "\tGot: " + str(train) + "\tError: " + str(error) + "\tFile: " + (w_files_train + w_files_dev)[0])
		train_err += error

	print("TESTING with test data")

	for index in range(len(test_input_data)):
		train = net.sim([test_input_data[index]])[0][0]
		error = round(abs(abs(train) - abs(test_output_data[index][0])), 3)
		print("Excepted: " + str(test_output_data[index][0]) + "\tGot: " + str(train) + "\tError: " + str(error) + "\tFile: " + (w_non_files_train + w_non_files_dev)[0])
		test_err += error

	print("TESTED")

	print("TRAIN DATA RECONGNITION ERROR: " + str(round(train_err / len(w_files_train + w_files_dev), 3)))
	print("TEST DATA  RECONGNITION ERROR: " + str(round(test_err / len(w_non_files_train + wnon__files_dev), 3)))

	print("PROCESSED")

	return 0

# Pokud je soubor hlavni a je v nem main, jinak odstranit
if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
