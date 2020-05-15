# search for an uploaded image by comparing its features
# to the features of every image in the index
# return a sorted list of the most similar images in the index

import numpy as np
import csv

class Searcher:
	def __init__(self, indexPath):
		self.indexPath = indexPath

	# compare the upload with every image in the index
	def search(self, queryFeatures, limit=10):
		results = {}
		with open(self.indexPath) as f:
			reader = csv.reader(f)
			i = 0
			for row in reader:
				d = 11.0
				try:
					features = [float(x) for x in row[1:]]
					d = self.chi2_distance(features, queryFeatures)
				except:
					pass
				if d < 10.0:
					results[row[0]] = d
				if d < 1.0:
					break
				i += 1
				if (i % 1000) == 0:
					print(i)
			f.close()
		results = sorted([(v, k) for (k, v) in results.items()])
		return results[:limit]

	# compute the chi-squared distance between features
    # represents similarity between the uploaded and indexed image
	def chi2_distance(self, histA, histB, eps=1e-10):
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
		return d


