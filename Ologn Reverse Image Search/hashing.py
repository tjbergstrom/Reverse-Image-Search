# hashing.py
# June 22, 2020
# these are hashing operations


import numpy as np
import cv2

def hash_distance(image, hashSize=8):
	# pre-process the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	resized = cv2.resize(gray, (hashSize + 1, hashSize))
	# compute the horizontal gradient between adjacent column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


# convert the hash to a NumPy 64-bit float and then back to int
def convert_hash(h):
	return int(np.array(h, dtype="float64"))


# compute the Hamming distance between integers
def hamming(a, b):
	return bin(int(a) ^ int(b)).count("1")


