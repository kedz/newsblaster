# Bag of Words (BoW) Model for Chained Classifier
#
# Use BoW model to calculate cosine distances
# between predicted titles and all meta tags.
#
# Ramzi Abdoch

# Utilities
import sys
import os

# Beautiful Soup
from bs4 import BeautifulSoup

class BoWser():

	def __init__(filename):
		soup = BeautifulSoup(filename)
		self.soup = soup

	def prep():
		metas = soup.find_all("meta")

		for tag in metas:
			print tag.get("content")

		# Isolate <meta> from soup

		# Tokenize Input

		# Create BoW
		# all_metas = [<meta> tag, BoW for text]

	# Calculate Cosine Diff between two BoWs
	def cos_dist():
		pass

if __name__ = "__main__":
	jr = BoWser(sys.argv[1])
	jr.prep()
