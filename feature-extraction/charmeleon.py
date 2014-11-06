from bs4 import BeautifulSoup
soup = BeautifulSoup(open("test.annotation"))

annotation_soup = BeautifulSoup('<p annotation="">test</p>')
annotation_tag = annotation_soup.tag

def has_annotation(tag):
    return tag.has_attr('annotation')

for annotation in soup.find_all(has_annotation):
    print(annotation)

# Setup hashmap for counts

# Iterate through links, calculate map for each node

# Use SciKit to store feature vectors for each annotated node

# Output X = [feature vectors], Y = [labels]