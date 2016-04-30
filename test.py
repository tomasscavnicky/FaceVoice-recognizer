from sklearn.decomposition import RandomizedPCA
from PIL import Image
import numpy
import glob
import math
import os.path
import string


 

IMG_RES = 80 * 80
NUM_EIGENFACES = 17 # num of features extracted from training images
NUM_TRAINIMAGES = 152 # num of training images

 
X = numpy.zeros([NUM_TRAINIMAGES, IMG_RES], dtype='int8') # training images
y = numpy.zeros(NUM_TRAINIMAGES) # labels





folder_name = "faces/"
test_positive_faces = os.listdir(folder_name)
imnbr_pos = len(test_positive_faces)

target = numpy.array([numpy.array(Image.open(folder_name+test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')


folder_name = "non_target_train/"
test_positive_faces = os.listdir(folder_name)
imnbr_pos = len(test_positive_faces)

non_target = numpy.array([numpy.array(Image.open(folder_name+test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')


X = numpy.concatenate((target, non_target), axis=0)


target_labels = numpy.ones(NUM_TRAINIMAGES-132)
non_target_labels = numpy.zeros(NUM_TRAINIMAGES-20)

y = numpy.append(target_labels, non_target_labels)


# extracting features from training images
pca = RandomizedPCA(n_components=NUM_EIGENFACES, whiten=True).fit(X)
X_pca = pca.transform(X)

# load test faces
test_faces = glob.glob('test_faces/*')

# create an array with flattened images located in folder folder_name
X = numpy.zeros([len(test_faces), IMG_RES], dtype='int8')

folder_name = "faces_dev/"
test_positive_faces = os.listdir(folder_name)
imnbr_pos = len(test_positive_faces)

X = numpy.array([numpy.array(Image.open(folder_name+test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')

# run through test images
for j, ref_pca in enumerate(pca.transform(X)):
    distances = []
    # calculate euclidian distance from test image to each of the known images and save distances
    for i, test_pca in enumerate(X_pca):
        dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
        distances.append((dist, y[i]))
 
    found_ID = min(distances)[1]
    print("Identified (result: "+ str(found_ID) +" - dist - " + str(min(distances)[0])  + ")")