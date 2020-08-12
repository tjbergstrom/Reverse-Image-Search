# search.py
# June 22, 2020
# upload a photo and find it in the directory
# also find some similar photo
# arg -d is the hash distance, increase it to find more similar photos

# python3 search.py -u uploads/img_01.jpg


from imutils import build_montages
from hashing import hash_distance
from hashing import convert_hash
import argparse
import pickle
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--upload", required=True, type=str)
ap.add_argument("-d", "--distance", type=int, default=10)
args = vars(ap.parse_args())

tree = pickle.loads(open("vptree.pickle", "rb").read())
hashes = pickle.loads(open("hashes.pickle", "rb").read())
image = cv2.imread(args["upload"])
distance = args["distance"]

# compute the hash for the upload and convert it
queryHash = hash_distance(image)
queryHash = convert_hash(queryHash)

# search
start = time.time()
results = tree.get_all_in_range(queryHash, distance)
results = sorted(results)
end = time.time()
print("Search Time =", (end - start))

# display results
i = 0
similars = []
for (d, h) in results:
	resultPaths = hashes.get(h, [])
	for resultPath in resultPaths:
		if i < 10:
			result = cv2.imread(resultPath)
			print("Result Location:", resultPath)
			result = cv2.resize(result, (600, 400))
			if i < 1:
				cv2.imshow(resultPath, result)
			else:
				similars.append(result)
			i += 1

if len(similars) > 0:
	montage = build_montages(similars, (128, 128), (3, 3))[0]
	cv2.imshow("Similar Images", montage)
cv2.waitKey(0)


