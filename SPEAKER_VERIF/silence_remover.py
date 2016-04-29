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

import struct, getopt, sys, os, re, numpy as np, wave

def is_silence(segment, trashhold = 100):

	energy = int(0)

	trashhold *= trashhold

	for point in segment:
		energy += point ** 2

	if(energy > trashhold):
		return segment
	else:
		return []

def wav_to_short(wave_file):

        # Library wave 
        w = wave.open(wave_file)

        # Starting from 1. sec because of booms
        if(16000 >= w.getnframes()):
                return

        length = w.getnframes() - 16000

        w.setpos(16000)
        wav_samples = w.readframes(length)

        # Library struct 
        short_samples = struct.unpack("%ih" % (length* w.getnchannels()), wav_samples)
        return np.asarray(short_samples)

def short_to_wav(wave_file, data):

	w = wave.open(wave_file, "w")

	w.setnchannels(1)
	w.setframerate(16000)
	w.setsampwidth(2)
	w.setnframes(len(data))

	for frame in data:
		print(frame)
		fr = struct.pack("h", frame)
		w.writeframes(fr)

	w.close()

def remove_silence(signal, frame_len = 400, trashhold = 100):

	processed_signal = list()

	if(len(signal) <= frame_len):
		return signal

	for segment_index in range(len(signal) / frame_len):

		processed_signal += is_silence(signal[(segment_index * frame_len):((segment_index + 1)* frame_len)], trashhold)

	return processed_signal

def main(args, argv):

	if(args != 2):
		exit(1)

	w_file = argv[0]
	w_trashhold = int(argv[1])

	signal = list(wav_to_short(w_file))

	new_signal = remove_silence(signal, frame_len = 400, trashhold = w_trashhold)

	short_to_wav("unsilenced.wav", new_signal)	

	print(len(signal))
	print(len(new_signal))

# Pokud je soubor hlavni a je v nem main, jinak odstranit
if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])
# End of file << file name >>
