# Article Annotator Server
#
# @Author - Ramzi Abdoch
#
# This server is meant to facilitate human
# annotation of HTML articles for use in the
# Newsblaster system.
#
# Flow:
#   1. users start the server by calling
#		- python annotator.py <source_dir> <dest_dir>
#		- <source_dir> is the directory where your HTML files reside
#		- <dest_dir> is the directory where .annotation files are saved
#	2. users can request /todo or /done to see a list
#		of articles that need annotation and have been
#		annotated already
#	3. from the /todo page, users can select an article and route to 
#		/annotate/<article_path>
#		- <article_path> is the path of the article in the <source_dir>
#

# To iterate through folder
import sys
import os

source_dir = sys.argv[1]
dest_dir = sys.argv[2]

from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# List unannotated articles
@app.route('/todo')
def todo(a=None):
	a = list()

	for filename in os.listdir(sys.argv[1]):
		print filename
		a.append(filename)

	return render_template('todo.html', a=a)

# List annotated articles
@app.route('/done')
def done(name=None):
	return render_template('hello.html', name="Ramzi Abdoch")

# Annotate an article
@app.route('/annotate/<article_path>')
def annotate(article_path):

	path = os.path.join(source_dir, article_path)

	fo = open(path)
	contents = fo.read();

	print contents

	# Close opened file
	fo.close()

	return render_template('annotate.html', path=path)

# Retrieve an article's text
@app.route('/text/<article_path>')
def get_text(article_path):
	pass

# View an annotated article
@app.route('/view/<article_path>')
def view(article_path):
	pass

if __name__ == '__main__':
    app.run(debug=True)