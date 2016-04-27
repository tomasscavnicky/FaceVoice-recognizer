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


def wav_to_mfcc(path, w_files, mfcc_output, frame_len = 400, trashhold = 2000, sampling = 16000):

	files = list()

	for w_file in sorted(w_files):

		if not (w_file.endswith(".wav")):
		        continue

		print("Processing: " + w_file)

		#content = list(wav_to_short(path + w_file, sampling))
		content = short_to_unsilenced_short(list(wav_to_short(path + w_file, sampling)), frame_len, trashhold)

		files.append(path + w_file)
		mfcc_output.append(short_to_mfcc(content, sampling).tolist()[0])

	return files


def short_to_mfcc(signal, sampling = 16000):

	mfcc_features = mfcc(np.asarray(signal), samplerate=sampling, winlen=0.025, winstep=0.01, numcep=13, nfilt=23, nfft=512, lowfreq=32, highfreq=(sampling/2), preemph=0.97, ceplifter=22, appendEnergy=True)
	#fbank_features = logfbank(np.asarray(signal), sampling)

	#return fbank_features[1:3,:]
	#return fbank_features[1:2,:]
	#r-eturn fbank_features[2:3,:]
	#print(np.shape(mfcc_features))
	#print("MFCC: " + str(mfcc_features))

	print(np.shape(mfcc_features))
	#print(np.shape(mfcc_features[0:1,:]))

	for X in mfcc_features:
		

	#for index in range(np.shape(mfcc_features)):
		

	#mffcc_features[0] = np.average(mffc_features[0]

	return mfcc_features[0:1,:]

def is_silence(segment, trashhold = 100):

	energy = int(0)
	trashhold *= trashhold

	for point in segment:
		energy += point ** 2

	if(energy > trashhold):
		return segment
	else:
		return []


def short_to_unsilenced_short(signal, frame_len = 400, trashhold = 100):

	processed_signal = list()

#	print(signal)

	if(len(signal) <= frame_len):
		return signal

	for segment_index in range(len(signal) / frame_len):

		processed_signal += is_silence(signal[(segment_index * frame_len):((segment_index + 1)* frame_len)], trashhold)

#	print("OLD LENGTH: " + str(len(signal)))
#	print("NEW LENGTH: " + str(len(processed_signal)))

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

#	print("OLD LENGTH: " + str(len(signal)))
#	print("NEW LENGTH: " + str(len(unsilenced_signal)))

	exit(0)

# Pokud je soubor hlavni a je v nem main, jinak odstranit
if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
