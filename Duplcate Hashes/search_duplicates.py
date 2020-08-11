# search_duplicates.py
# August 10, 2020
# input a dataset and find duplicates
# generate hashes for each image to find duplcate hashes
# important for ML projects because duplicates can cause bias
#
# python3 search_duplicates.py -d dataset
# optional arg -s to display the duplicates for assurance
# optional arg -r to actually remove duplicates for safety

from imutils import paths
import numpy as np
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True)
ap.add_argument("-r", "--remove", type=bool, default=False)
ap.add_argument("-s", "--show", type=bool, default=True)
args = vars(ap.parse_args())
hash_size = 8

# paths to all images in the input dataset
img_paths = list(paths.list_images(args["dataset"]))
# dictionary of hashes of the images
hashes = {}

# part one, loop through the input images and generate their hashes
print("Generating Hashes...")
for img_path in img_paths:
	image = cv2.imread(img_path)
	# convert the image to grayscale - smaller and easier to work with
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# resize with a single column (width)
	resized = cv2.resize(gray, (hash_size + 1, hash_size))
	# compute a horizontal gradient between adjacent column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	img_hash = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
	# find any other image paths with the same hash and add the current image
	paths = hashes.get(img_hash, [])
	# and store the list of paths back in the hashes dictionary
	paths.append(img_path)
	hashes[img_hash] = paths

# part two, loop through the hashes and find duplicates
print("Finding Duplicates...")
for (img_hash, hashed_paths) in hashes.items():
	# is there more than one image with the same hash
	if len(hashed_paths) > 1:
		# display the duplicates
		if args["show"]:
			montage = None
			for path in hashed_paths:
				image = cv2.imread(path)
				image = cv2.resize(image, (150, 150))
				if montage is None:
					montage = image
				else:
					montage = np.hstack([montage, image])
			cv2.imshow("Duplicates", montage)
			cv2.waitKey(0)
		# remove the duplicates
		if args["remove"]:
			for path in hashed_paths[1:]:
				os.remove(path)
				print("Duplicate image" + path + "was deleted")



