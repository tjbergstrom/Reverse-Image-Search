# search.py
# June 2020
# Upload a photo and find the best match in the index
# Also find some similar photos
#
# $ python3 search.py -u uploads/img_01.jpg


from imutils import build_montages
from hashing import hash_distance
from hashing import convert_hash
import argparse
import imutils
import pickle
import time
import cv2
import sys
import os


def search(tree, query, dist=30):
	start = time.time()
	results = sorted(tree.get_all_in_range(query, dist))
	end = time.time()
	print(f"Found {len(results)} results in {end - start} seconds")
	return results


def get_imgs(search_results, hashes):
	img_paths = []
	for point, idx in search_results: # O(len(search_results))
		loc = hashes.get(idx, [])
		for img_path in loc: # O(1) unless duplicate images at this index
			img_paths.append(img_path)
	return img_paths


def display(img_paths):
	img_path = img_paths.pop(0)
	print(f"Best Match: {img_path}")
	cv2.imshow(img_path, imutils.resize(cv2.imread(img_path, 500)))
	if len(img_paths) > 0:
		similars = [cv2.imread(i) for i in img_paths]
		montage = build_montages(similars, (128, 128), (3, 3))[0]
		cv2.imshow("Similar Images", montage)
		print("Similar Images:")
		for i in img_paths:
			print(f" {i}")
	cv2.waitKey(0)


def check(img_path):
	if not os.path.isfile(img_path):
		sys.exit(1)
	filename, ext = os.path.splitext(img_path)
	if ext not in [".jpg", ".jpeg", ".png", ".bmp"]:
		sys.exit(1)
	return img_path


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-u", "--upload", required=True, type=str)
	args = vars(ap.parse_args())
	img_path = check(args["upload"])

	tree = pickle.loads(open("vptree.pickle", "rb").read())
	hashes = pickle.loads(open("hashes.pickle", "rb").read())

	query_hash = hash_distance(img_path)
	query_idx = convert_hash(query_hash)

	search_results = search(tree, query_idx)
	img_paths = get_imgs(search_results, hashes)
	display(img_paths)



##
