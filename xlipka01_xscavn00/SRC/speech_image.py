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

import sys, os, numpy as np

# Input arguments: Speech_log_file, Image_log_file, Output_log_file

def main(args, argv):

	if(args != 2):
		exit(1)

	try: 
		speech_file = open(argv[0], "r")
		image_file = open(argv[1], "r")

	speech_data = speech_file.readlines().split(' ')
	image_data = image_file.readlines().split(' ')

	min_image = max(image_data[]



if __name__ == '__main__':
	main(len(sys.argv) - 1, sys.argv[1:])

# End of file << file name >>
