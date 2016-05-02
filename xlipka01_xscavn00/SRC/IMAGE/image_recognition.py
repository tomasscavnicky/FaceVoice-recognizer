#!/usr/bin/env python3

# Project: Person recognition, IKR
# Description: Extrakce a porovnavani priznaku z obrazku
# Author: Radim Lipka, Tomas Scavincky
# Email: xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz
# Date: 29.4.2016
# File: image_recognition.py

__author__ = "Radim Lipka, Tomas Scavincky"
__version__ = "1.0"
__email__ = "xlipka01@stud.fit.vutbr.cz, xscavn00@stud.fit.vutbr.cz"
__date__ = "29.4.2016"


from sklearn.decomposition import RandomizedPCA
from PIL import Image
import numpy
import glob
import math
import os.path, sys
import string
import re
from math import floor
from pprint import pprint
import matplotlib.pyplot as plt


def load_images(folder_name):
	faces = os.listdir(folder_name)
	imnbr_pos = len(test_positive_faces)
	final_array = numpy.zeros([imnbr_pos, 80*80])

	for face in faces:
		i = Image.open(folder_name+face)
		i = numpy.array(i)
		i[:,:,0] *=3
		i = Image.fromarray(i).convert('L')
		i = numpy.array(i).flatten()
		final_array = numpy.append(final_array, i)
	return final_array


def plot_gallery(images, titles, h, w, n_row=4, n_col=5):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())


# SET THESE TWO VARIABLES
train_target_folder = "../../DATA/target_train/" # <-- folder with target training faces
train_non_target_folder = "../../DATA/non_target_train/" # <-- folder with non target training faces



IMG_RES = 80 * 80
NUM_EIGENFACES = 20 # num of features extracted from training images
NUM_TRAINIMAGES = 444 # num of training images
DISTANCE_THRESHOLD = 3.0

 
X = numpy.zeros([NUM_TRAINIMAGES, IMG_RES], dtype='int8') # training images
y = numpy.zeros(NUM_TRAINIMAGES) # labels



def train_and_classify(filepath_to_classification_folder):
	if filepath_to_classification_folder[-1] != '/':
		filepath_to_classification_folder += '/'


	folder_name = train_target_folder
	test_positive_faces = glob.glob(folder_name+"*.png")
	imnbr_pos = len(test_positive_faces)

	target = numpy.array([numpy.array(Image.open(test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')


	folder_name = train_non_target_folder
	test_positive_faces = glob.glob(folder_name+"*.png")
	imnbr_pos = len(test_positive_faces)

	non_target = numpy.array([numpy.array(Image.open(test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')


	X = target # numpy.concatenate((target, non_target), axis=0)


	target_labels = numpy.ones(NUM_TRAINIMAGES-384)
	non_target_labels = numpy.zeros(NUM_TRAINIMAGES-60)

	y = numpy.append(target_labels, non_target_labels)


	# extracting features from training images
	pca = RandomizedPCA(n_components=NUM_EIGENFACES, whiten=True).fit(X)
	X_pca = pca.transform(X)

	# eigenfaces = pca.components_.reshape((NUM_EIGENFACES, 80, 80))
	# eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
	# plot_gallery(eigenfaces, eigenface_titles, 80, 80)
	# plt.show()
	# exit()


	# load test faces
	test_faces = glob.glob('test_faces/*')

	# create an array with flattened images located in folder filepath_to_classification_folder given by argument of the script
	X = numpy.zeros([len(test_faces), IMG_RES], dtype='int8')

	folder_name = filepath_to_classification_folder
	test_positive_faces = glob.glob(folder_name+"*.png")
	imnbr_pos = len(test_positive_faces)

	X = numpy.array([numpy.array(Image.open(test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')

	# face classification
	results = []
	
	for j, ref_pca in enumerate(pca.transform(X)):
	    distances = []
	    # calculate euclidian distance from test image to each of the known images and save distances
	    for i, test_pca in enumerate(X_pca):
	        dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
	        distances.append(dist)

	    found_distance = min(distances)
	    file_name = re.search('/([^/]+).png', test_positive_faces[j]).group(1)
	    hard_decision = 1 if found_distance <= DISTANCE_THRESHOLD else 0
	    confidence = found_distance / DISTANCE_THRESHOLD if hard_decision == 1 else DISTANCE_THRESHOLD / found_distance
	    results.append((file_name, found_distance, hard_decision))
	return results
	
	

if __name__ == "__main__": 
	results = train_and_classify(sys.argv[1])
	formated_results = []
	for elem in results:
		formated_results.append(' '.join(str(i) for i in elem))
	results = '\n'.join(formated_results)
	if len(sys.argv) >= 3:
		fp = open(sys.argv[2], 'w')
		fp.write(results)
		fp.close()
	else:
		print(results)