
# run this file to set up an index of images to search thru
# run: python3 index.py --dataset dataset --index index.csv
# this will take all photos from your dataset and save 
# the each filename with its feature vector in the index.csv file



from pyimagesearch.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

cd = ColorDescriptor((8, 12, 3))
output = open(args["index"], "w")

# use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.png"):
	# extract the image filename) 
	imageID = imagePath[imagePath.rfind("/") + 1:]
	image = cv2.imread(imagePath)
	features = cd.describe(image)
	# write the features to file
	features = [str(f) for f in features]
	output.write("%s,%s\n" % (imageID, ",".join(features)))

output.close()
