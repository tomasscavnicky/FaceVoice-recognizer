#!/usr/bin/env python3

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

def wav_to_short(wave_file):

	# Library wave 
	w = wave.open(wave_file)
	astr = w.readframes(w.getnframes())

	# Library struct 
	a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
	return a


def main(args, argv):

	if(args != 1):
		exit(1)

	try:
		w_files = os.listdir(argv[0])
	except:
		exit(2)

	for w_file in w_files:

		if not (w_file.endswith(".wav")):
			continue

		print("Processing: " + w_file)
		content = wav_to_short(argv[0] + w_file)

	print("KONEC")

	return 0


# Pokud je soubor hlavni a je v nem main, jinak odstranit
if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
