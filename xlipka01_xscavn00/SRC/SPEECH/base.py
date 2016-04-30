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

import matplotlib.pyplot as plt

def wav_to_mfcc(path, w_files, mfcc_output, frame_len = 400, trashhold = 3500, sampling = 16000):

	files = list()

	for w_file in sorted(w_files):

		if not (w_file.endswith(".wav")):
		        continue

		print("Processing: " + w_file)

		content = short_to_unsilenced_short(list(wav_to_short(path + w_file, sampling)), frame_len, trashhold)

		files.append(path + w_file)
		mfcc_output.append(short_to_mfcc(content, sampling).tolist())

	return files


def short_to_mfcc(signal, sampling = 16000):

	mfcc_features = mfcc(np.asarray(signal), samplerate=sampling, winlen=0.025, winstep=0.015, numcep=26, nfilt=26, nfft=512, lowfreq=32, highfreq=2000, preemph=0.97, ceplifter=22, appendEnergy=True)
		
	Priznaky = np.ones(np.shape(mfcc_features)[1])

	Priznaky = np.average(mfcc_features, axis = 0)[1:13]
	
	return np.array(Priznaky)


def is_silence(segment, trashhold = 2000):

	energy = int(0)
	trashhold *= trashhold

	for point in segment:
		energy += point ** 2

	if(energy > trashhold):
		return segment
	else:
		return []


def short_to_unsilenced_short(signal, frame_len = 400, trashhold = 2000, framerate = 16000):

	processed_signal = list()

	if(len(signal) <= frame_len):
		return signal

	indent = framerate

	for segment_index in range((((len(signal) - indent)) / frame_len) - 1):

		processed_signal += is_silence(signal[indent:indent + frame_len], trashhold)
		indent += frame_len

	return processed_signal


def wav_to_short(wave_file, framerate):

        # Library wave 
        w = wave.open(wave_file)

        # Starting from 1. sec because of booms
        if(framerate >= w.getnframes()):
                return

        length = w.getnframes() - framerate

        w.setpos(framerate)
        wav_samples = w.readframes(length)

        # Library struct 
        short_samples = struct.unpack("%ih" % (length* w.getnchannels()), wav_samples)
        return np.asarray(short_samples)


def short_to_wav(data, w_file = "unsilenced.wav", frame_rate = 16000, channels = 1, sample_width = 2):

	w = wave.open(w_file, "w")

	w.setnchannels(channels)
	w.setframerate(frame_rate)
	w.setsampwidth(sample_width)

	w.setnframes(len(data))

	for dato in data:
		fr = struct.pack("h", dato)
		w.writeframes(fr)

	w.close()


def main(args, argv):

	if(args != 2):
		exit(1)

	w_file = argv[0]
	w_trashhold = int(argv[1])

	signal = list(wav_to_short(w_file, 16000))

	unsilenced_signal = short_to_unsilenced_short(signal, frame_len = 400, trashhold = w_trashhold)

	short_to_wav(unsilenced_signal, "unsilenced.wav", 16000, 1, 2)

	exit(0)

if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
