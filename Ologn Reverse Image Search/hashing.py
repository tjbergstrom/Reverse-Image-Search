# hashing.py
# June 2020
# Some hashing operations


import numpy as np
import cv2


def hash_distance(img_path, hash_size=16):
	""" Convert an image to a hash """
	img = cv2.imread(img_path)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (hash_size + 1, hash_size))
	# The horizontal gradients between adjacent column pixels
	diff = img[:, 1:] > img[:, :-1]
	# Convert the difference to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
	""" Get the int table index from a NumPy 64-bit float hash """
	return int(np.array(h, dtype="float64"))


def hamming(a, b):
	""" To compute the Hamming distance between 2 integers """
	return bin(int(a) ^ int(b)).count("1")



##
