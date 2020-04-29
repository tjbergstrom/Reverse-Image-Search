# upload an image and search for it
# display the best match and its location
# also display up to 9 similar images

# python3 search.py -u uploads/img.jpg
# python3 search.py -u uploads/img.jpg -i index.csv -r dataset

# -u = path to the image you want to upload
# -i = path to the csv index containing all feature vectors
# -r = path to the found photos in the dataset

from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
from imutils import build_montages
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--result-path", type=str, default="photos")
ap.add_argument("-i", "--index", type=str, default="index.csv")
ap.add_argument("-u", "--upload", required = True)
args = vars(ap.parse_args())

cd = ColorDescriptor((8, 12, 3))
upload = cv2.imread(args["upload"])
features = cd.describe(upload)
searcher = Searcher(args["index"])
results = searcher.search(features)

i = 0
locs = []
similars = []
print(len(results))
for (score, resultID) in results:
	location = args["result_path"] + "/" + resultID
	result = cv2.imread(location)
	if(i<1):
		title = "Best Match: " + location
		im = cv2.resize(result, (600, 400))
		cv2.imshow(title, im)
		cv2.waitKey(0)
		i = 1
	else:
		similars.append(result)
		locs.append(location)


montage = build_montages(similars, (128, 128), (3, 3))[0]
cv2.imshow("Similar Images", montage)
print(locs)
cv2.waitKey(0)



