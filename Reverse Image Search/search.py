# upload an image and search for it
# display the best match and its location
# also display 9 similar images

# python3 search.py -u uploads/img.jpg
# python3 search.py -u uploads/img.jpg -i index.csv

# -u = path to the image you want to upload
# -i = path to the csv index containing all feature vectors

from imgsearch.colordescriptor import ColorDescriptor
from imgsearch.searcher import Searcher
from imutils import build_montages
import argparse
import cv2

ap = argparse.ArgumentParser()
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
for (score, resultID) in results:
	result = cv2.imread(resultID)
	if(i<1):
		if score < 1.0:
			title = "Found: " + resultID
		else:
			title = "Not Found - Best Match: " + resultID
		im = cv2.resize(result, (600, 400))
		cv2.imshow(title, im)
		#cv2.waitKey(0)
		i = 1
	else:
		similars.append(result)
		locs.append(resultID)
	print(resultID, "-", score)


montage = build_montages(similars, (128, 128), (3, 3))[0]
cv2.imshow("Similar Images", montage)
im = cv2.resize(upload, (600, 400))
cv2.imshow(args["upload"], im)
cv2.waitKey(0)



