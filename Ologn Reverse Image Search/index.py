# index.py
# June 22, 2020
# take an input directory of photos
# compute their hashes
# save a VP-tree of hashes
# a vantage-point tree is a data structure that reduces search time to O(logn)
# it takes a position and splits the data points into near/far from the point
# and it does this recursively splitting into smaller sets
# so that neighbors have smaller distances

# python3 index.py -d photos


from hashing import hash_distance
from hashing import convert_hash
from hashing import hamming
from imutils import paths
import argparse
import pickle
import vptree
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, type=str)
args = vars(ap.parse_args())

imagePaths = list(paths.list_images(args["dataset"]))
hashes = {}

# compute the hashes of the images and add them to the directory
for (i, imagePath) in enumerate(imagePaths):
	image = cv2.imread(imagePath)
	h = hash_distance(image)
	h = convert_hash(h)
	l = hashes.get(h, [])
	l.append(imagePath)
	hashes[h] = l

# build and save the VP-Tree of the hashes
points = list(hashes.keys())
tree = vptree.VPTree(points, hamming)
f = open("vptree.pickle", "wb")
f.write(pickle.dumps(tree))
f.close()
f = open("hashes.pickle", "wb")
f.write(pickle.dumps(hashes))
f.close()


