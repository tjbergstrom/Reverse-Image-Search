# make an index of feature vectors of every photo in a dataset
# including all sub directories
# the search uses that index to find images

# python3 index.py
# python3 index.py -d photos -i index.csv

from imgsearch.colordescriptor import ColorDescriptor
from imutils import paths
import argparse
import glob
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", type=str, default="photos")
ap.add_argument("-i", "--index", type=str, default="index.csv")
args = vars(ap.parse_args())

imagePaths = paths.list_images(args["dataset"])
cd = ColorDescriptor((8, 12, 3))
output = open(args["index"], "w")

for imagePath in imagePaths:
	imageID = imagePath
	image = cv2.imread(imagePath)
	features = cd.describe(image)
	features = [str(f) for f in features]
	output.write("%s,%s\n" % (imageID, ",".join(features)))
	print(imageID)

output.close()



