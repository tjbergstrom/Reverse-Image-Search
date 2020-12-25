# search_duplicates.py
# August 10, 2020
# input a dataset and find duplicates
# generate hashes for each image to find duplcate hashes
# important for ML projects because duplicates can cause bias
#
# python3 search_duplicates.py -d dataset
# optional arg -s to display the duplicates for assurance
# optional arg -r to actually remove duplicates for safety


from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import cv2
import sys
import os


def generate(img_paths, hash_size=16):
	hashes = {}
	for img_path in img_paths:
		img = cv2.imread(img_path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.resize(img, (hash_size + 1, hash_size))
		diff = img[:, 1:] > img[:, :-1]
		idx = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
		loc = hashes.get(idx, [])
		loc.append(img_path)
		hashes[idx] = loc
	return hashes


def find_duplicates(hashes, show, remove):
	for idx, loc in hashes.items():
		if len(loc) > 1:
			if show:
				duplicates = [cv2.imread(i) for i in loc]
				montage = build_montages(duplicates, (128, 128), (3, 3))[0]
				cv2.imshow("Duplicates", montage)
				if cv2.waitKey(900) == ord("s"):
					continue
			if remove:
				for img_path in loc[1:]:
					os.remove(img_path)
					print(f"Duplicate {img_path} was deleted")


def check(dataset):
	img_paths = list(paths.list_images(args["dataset"]))
	if len(img_paths) > 0:
		return img_paths
	else:
		print(f"No images found in {dataset}")
		sys.exit(1)


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dataset", required=True)
	ap.add_argument("-r", "--remove", type=bool, default=False)
	ap.add_argument("-s", "--show", type=bool, default=True)
	args = vars(ap.parse_args())

	img_paths = check(args["dataset"])

	hashes = generate(img_paths)

	find_duplicates(hashes, args["show"], args["remove"])



##
