from PIL import Image
import numpy
import matplotlib.pylab as pylab
import os
from operator import mul
from functools import reduce

from sklearn.grid_search import GridSearchCV
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC


def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
    """Helper function to plot a gallery of portraits"""
    pylab.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    pylab.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        pylab.subplot(n_row, n_col, i + 1)
        pylab.imshow(images[i].reshape((h, w)), cmap=pylab.cm.gray)
        pylab.title(titles[i], size=12)
        pylab.xticks(())
        pylab.yticks(())



def pca(X):
  # Principal Component Analysis
  # input: X, matrix with training data as flattened arrays in rows
  # return: projection matrix (with important dimensions first),
  # variance and mean

  #get dimensions
  num_data,dim = X.shape

  #center data
  mean_X = X.mean(axis=0)
  for i in range(num_data):
      X[i] -= mean_X

  if dim>100:
      M = numpy.dot(X,X.T) #covariance matrix
      e,EV = numpy.linalg.eigh(M) #eigenvalues and eigenvectors
      tmp = numpy.dot(X.T,EV).T #this is the compact trick
      V = tmp[::-1] #reverse since last eigenvectors are the ones we want
      S = numpy.sqrt(e)[::-1] #reverse since eigenvalues are in increasing order
  else:
      print('PCA - SVD used')
      U,S,V = linalg.svd(X)
      V = V[:num_data] #only makes sense to return the first num_data

  #return the projection matrix, the variance and the mean
  return V,S,mean_X



def compare_images(folder_name):
	test_positive_faces = os.listdir(folder_name)
	im_pos = numpy.array(Image.open(folder_name+test_positive_faces[0]).convert('L'))
	m_pos, n_pos = im.shape[0:2]
	imnbr_pos = len(test_positive_faces) #get the number of images

	target_train_pos = numpy.array([numpy.array(Image.open(folder_name+test_positive_faces[i]).convert('L')).flatten() for i in range(imnbr_pos)],'f')

	V_pos,S_pos,immean_pos = pca(target_train_pos)

	immean_pos = immean_pos.reshape(m_pos,n_pos)

	n_eigenf = 10 if imnbr_pos >= 10 else imnbr_pos

	x = reduce(mul, (V_pos[:n_eigenf] - V[:n_eigenf])**2, 1)
	return x


def compare_image(image_name):
	im_pos = numpy.array(Image.open(image_name).convert('L'))
	m_pos, n_pos = im.shape[0:2]
	imnbr_pos = 1 #get the number of images

	target_train_pos = numpy.array([numpy.array(Image.open(image_name).convert('L')).flatten()],'f')

	V_pos,S_pos,immean_pos = pca(target_train_pos)

	immean_pos = immean_pos.reshape(m_pos,n_pos)

	n_eigenf = 10 if imnbr_pos >= 10 else imnbr_pos
	print("S_pos: "+str(S_pos))
	x = reduce(mul, (S_pos[:n_eigenf] - S[:n_eigenf])**2, 1)
	return x

def recognise(img):
	normal_img = img - immean
	M = numpy.dot(img, img.T)
	e,EV = numpy.linalg.eigh(M)
	tmp = numpy.dot(img.T, EV).T
	V = tmp[::-1]
	S = numpy.sqrt(abs(e))[::-1]









# CREATING MODEL

imlist = os.listdir('faces')
im = numpy.array(Image.open('faces/'+imlist[0]).convert('L')) #open one image to get the size
m,n = im.shape[0:2] #get the size of the images
imnbr = len(imlist) #get the number of images
target_train = numpy.array([numpy.array(Image.open('faces/'+imlist[i]).convert('L')).flatten() for i in range(imnbr)],'f')




V,S,immean = pca(target_train)
print(V)
exit()



immean = immean.reshape(m,n)
mode = V[0].reshape(m,n)

# pylab.figure()
# pylab.gray()
# pylab.imshow(immean)

# pylab.figure()
# pylab.gray()
# pylab.imshow(mode)

# pylab.show()

# exit()




# # IMAGES SEPARATELY

# for img_name in os.listdir("negative_faces2"):
# 	obrazok = numpy.array([numpy.array(Image.open("negative_faces2/"+img_name).convert('L')).flatten()])
# 	V_pos,S_pos,immean_pos = pca(obrazok)
# 	exit()
# 	x = reduce(mul, (obrazok[:20] - S[:n_eigenf])**2, 1)
# 	# x = compare_image("negative_faces2/"+img_name)
# 	print(img_name+":")
# 	print(x)
# exit()



# POSITIVE TEST IMAGES
for i in range(1,4):
	x = compare_images('positive_faces'+str(i)+'/')
	print("positive images results "+str(i)+":")
	print(numpy.mean(x))


# NEGATIVE TEST IMAGES


for i in range(1,11):
	x = compare_images('negative_faces'+str(i)+'/')
	print("negative images results "+str(i)+":")
	# is_face = True if x > 1e+54 else False
	print(numpy.mean(x))

# x = compare_images('negative_faces1/')
# print("negative images results 1:")
# print(x)

# x = compare_images('negative_faces2/')
# print("negative images results 2:")
# print(x)

# x = compare_images('negative_faces3/')
# print("negative images results 3:")
# print(x)




#show the images
# pylab.figure()
# pylab.gray()
# pylab.imshow(immean)

# for i in range(0,19):
# 	pylab.figure()
# 	pylab.gray()
# 	pylab.imshow(V[i].reshape(m,n))

# pylab.show()

# pylab.figure()
# pylab.gray()
# pylab.imshow(mode1)

# pylab.figure()
# pylab.gray()
# pylab.imshow(mode2)

# pylab.show()