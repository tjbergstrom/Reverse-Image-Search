


from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2

# define a function to extract a histogram from each
# channel of the image
def histogram(image):
	# initialize the list of histograms, one calculated
	# for each channel of the image
	hists = []

	# loop over the image channels
	for chan in cv2.split(image):
		# create a histogram for the current channel and
		hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
		hist = cv2.normalize(hist)
		hists.append(hist)

	# return the list of histograms
	return hists

# define a function used to rotate an image
def rotate(image, angle):
	# grab the dimensions of the image and calculate the
	# center of the image
	(h, w) = image.shape[:2]
	center = (w / 2, h / 2)

	# rotate and scale the image
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	affine = cv2.warpAffine(image, M, (w, h))

	# return the rotated and scaled image
	return affine

# define a funciton used to resize an image
def resize(image, scale):
	# calculate the dimensions of the new resized image and
	# then perform the resizing
	dim = tuple(np.int32((image.shape[0] * scale, image.shape[1] * scale)))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

	# return the resized image
	return resized

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

# loop over the list of rotations (in degrees) and scales
for (i, (angle, scale)) in enumerate(((0, 1.0), (90, 0.5), (180, 0.25))):
	# rotate and resize the image, then calculate a histogram
	# for each channel of the image
	affine = resize(rotate(image, angle), scale)
	hists = histogram(affine)

	# initialize the figure and show the resized image
	title = "Angle: %d, Scale: %.2f" % (angle, scale)
	plt.figure(title)
	cv2.imshow(title, affine)

	# loop over the histograms for each channel and plot them
	for (hist, color) in zip(hists, ("b", "g", "r")):
		plt.plot(hist, color = color)
		plt.xlim([0, 256])
		plt.ylim([0, 1])

# show the plots and wait for a keypress
plt.show()
cv2.waitKey(0)


