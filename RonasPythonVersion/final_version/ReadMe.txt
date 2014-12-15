Documentation for Program Clust

Description of Program
_______________________
This program clusters a set of input docs into super- and sub- clusters.
It is also designed to do incremental clustering, i.e. to cluster additional
input docs into a pre-existing set of super- and sub- clusters

Running the Program
___________________

The program assumes the documents to be clustered reside in a directory located
at path [rootdir]. This directory should contain each document as a separate file
within that folder. Each document merely consists of the body of the article. 

To run the program:
	python runner.py [-l load-clust] [-s save-clust] [-i segsize] [-r rootdir] [-f listfile]
		[-T major-threshold] [-t minor-threshold]
	
	** All paths are absolute paths. **
	
	Description of Mandatory Parameters
	___________________________________

	[listfile] is the path to the file in which the tf-idf and the IDs of 
	the documents should be saved. This file created during dataprep after 
	the tf-idfs are calculated and is read during clustering to calculate 
	cosine distances between documents.

	[rootdir] is the path to the folder containing the new documents to be 
	clustered. Each document should be a separate file within the folder.

	[major-threshold] is the cluster similarity value above which two existing
	super-clusters should be combined into a larger super-cluster. It is a floating
	point value between 0.0 and 1.0. Also, [major-threshold] should be less than or
	equal to [minor-threshold].

	[minor-threshold] is the cluster similarity value above which two existing 
	sub-clusters should be combined into a larger sub-cluster. It is a floating point
	value between 0.0 and 1.0

	Description of Optional Parameters
	__________________________________
	[load-clust] is the path containing a pre-existing set of super- and sub-
	clusters. Specifying this option means that the (new) input docs should be 
	added to these clusters if they are similar enough. Leaving out this option
	means that the input docs should be clustered only among themselves.

	[save-clust] is the path to which super- and sub- cluster information should
	be saved after al of the input docs have been so clustered. Leaving out this
	option has the consquence that any clusters created by the program cannot be 
	incrementally added to by a future invocation of the program.

	[segsize] is the number of docs to process in the inner loop of this algorithm.
	If the number of new documents is larger than the segsize, the new documents
	will be divided into segments of segsize and each of these will be clustered
	separately into superclusters, then these superclusters will be clustered with
	each other, and then subclusters will be found within these superclusters. If 
	this option is left out, the default value is defined as 10,000. 

Description of Outputs
______________________

After running runner.py, there will be 3 separate outputs.
	1. The tf-idfs and the idfs of the documents will be written to listfile.
	2. The output of the clustering will be displayed in a readable format in stdout.
	3. (Optional) The output of the clustering will be saved to save-clust in JSON.

	listfile Output
	_______________
	File is in JSON format. It contains a list of two elements. The first element
	is a list of document names where the index of the document is the ID of the
	document. The second element is a list of dictionaries. Each dictionary 
	corresponds the the document at the same index of the first list. Each dictionary
	contains key, value pairs in which the key is a unique word from the document
	and the value is the tf-idf value of that unique word in the document. Each
	word of the document, will be a key in the dictionary. This JSON formatted file
	is outputted during dataprep and read during clustering. 


	StdOut Output
	_____________
	This file lists a set of super- and sub-clusters.  Each supercluster
  	is identified with a header line that looks like this:

    	####### Similarity: <simval1> Superclustid: <superclustid1> <optional *>

  	<simval1> is the supercluster's similarity value.  <superclustid1> is
 	 this supercluster's id num; the id num identifies it uniquely out of
 	 all superclusters.  <optional *> may either be present or not.  If it is
  	present, that means that docs have been added to this supercluster
  	by the program run.  Conversely, if not present, that means that this
  	supercluster has not been added to.

  	The header line for a supercluster is followed by a list of subclusters
  	that this supercluster is fragmented into.  As is the case with each
  	supercluster, each subcluster is also identified with a header line:

    	$$$$$$$ Similarity: <simval1> Subclustid: <subclustid1> <optional *>

  	<simval1>, <subclustid1>, and <optional *> are fields that have meanings
  	analogous to the meanings of the similarly-named fields of the supercluster
  	header line.  Although each subcluster has an id num that uniquely
  	identifies it out of all subclusters, id nums across both super- and
  	sub- clusters may not be unique.

  	Each subcluster header line is followed by a list of names of docs
  	that comprise the subcluster, one per line, like this:

    	<docname1>
    	<docname2>
    	...
    	<docnameM>

  	Here is sample output of the program:

    	####### Similarity: 0.387426 Superclustid: 1 *
    	$$$$$$$ Similarity: 0.000000 Subclustid: 1 *
    	cbc.ca.1173.txt
    	$$$$$$$ Similarity: 0.000000 Subclustid: 15 *
    	cbc.ca.2653.txt
    	####### Similarity: 0.673973 Superclustid: 3 *
    	$$$$$$$ Similarity: 0.833366 Subclustid: 3 *
    	cbc.ca.1265.txt
    	cbc.ca.3628.txt
    	cbc.ca.1321.txt
    	cbc.ca.5106.txt
    	cbc.ca.5301.txt
    	$$$$$$$ Similarity: 0.865612 Subclustid: 11 *
    	cbc.ca.2240.txt
    	cbc.ca.3523.txt
    	$$$$$$$ Similarity: 0.000000 Subclustid: 14 *
    	cbc.ca.2647.txt

  	There are two superclusters, #1 and #3.  Supercluster #1 is divided
  	into two subclusters.  Supercluster #3 is divided into three
  	subclusters.

	Save-Clust Output
	_________________
	File is in JSON format. It consists of a list of superclusters in which
	each supercluster is of the format [list of docs in clust by id, clust id,
	supercluster's subclusts]. Each subclust in the supercluster is formatted 
	in the same way [list of docs in clust by id, clust id, empty list (because 
	no subclusts)].

Algorithm Overview
__________________
The algorithm is divided into two parts:
	1. Dataprep
	2. Clustering based on Cosine Distance

	DataPrep
	________
	Each document is read in, and tf-idfs are calculated using TfidfsVectorizer
	by sklearn. Each row is that converted into a dictionary and saved into listfile.
	
	Clustering
	__________
	Tf-idfs are read in from the listfile. If a load-clust is specified, that is 
	also read in. The first 101 words are used to calculate the cosine distances
	of the documents. The new documents are broken down into segments of segsize.
	Each segment is treated as follows. The documents are made into separate clusters.
	The document clusters are greedy merged into superclusters based on the major threshold.
	These superclusters are merged with the existing superclusters resulting in a cluster
	containing the old clusters and the new clusters. (Repeat for each segment). Once completed,
	the each supercluster's documents are made into separate clusters and greedy merged
	into subclusters based on the minor threshold. 

	The greedy merge works as follows. The distance between each clust is calculated and if
	this distance meets the given theshold, the pair of clusts is added to a heap sorted by 
	similarity. The most similar pair is poped off the heap and merged. Any pair on the heap
	that is affected by this merge is removed (i.e. the pair contains a clust that no longer 
	exists because of the merge). Distances to the new clust are calculated and if any of these
	distances meet the threshold, the pair is added to the heap. Repeat until there are no more
	clust pairs on the heap. 
