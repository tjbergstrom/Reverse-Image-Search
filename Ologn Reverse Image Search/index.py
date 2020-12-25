# index.py
# June 2020
# Take an input directory of photos and compute their hashes
# Save an index of the hashes (the hash table of all the image hashes)
# And save a VP-tree of the hashes for O(logn) search time to find similar hashes
#
# $ python3 index.py -d photos


from hashing import hash_distance
from hashing import convert_hash
from hashing import hamming
from imutils import paths
import argparse
import pickle
import vptree
import sys
import os


def compute_hashes(img_paths, hashes={}):
	for img_path in img_paths:
		hashed = hash_distance(img_path)
		idx = convert_hash(hashed)
		loc = hashes.get(idx, [])
		loc.append(img_path)
		hashes[idx] = loc
	return hashes


def save_tree(hashes):
	points = list(hashes.keys())
	tree = vptree.VPTree(points, hamming)
	f = open("vptree.pickle", "wb")
	f.write(pickle.dumps(tree))
	f.close()
	f = open("hashes.pickle", "wb")
	f.write(pickle.dumps(hashes))
	f.close()


def check(dataset):
	if not os.path.isdir(dataset):
		sys.exit(1)
	img_paths = list(paths.list_images(dataset))
	if len(img_paths) <= 0:
		sys.exit(1)
	return img_paths


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dataset", required=True)
	args = vars(ap.parse_args())

	img_paths = check(args["dataset"])
	hashes = compute_hashes(img_paths)
	save_tree(hashes)



##
