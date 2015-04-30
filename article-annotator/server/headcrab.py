# Headcrab.py - Finds headless annotations and attaches the original head... similar to a headcrab.
# Reference: http://en.wikipedia.org/wiki/Headcrab
# Author: Ramzi Abdoch

# Utilities
import os
import sys
import re

class HeadCrab():

    # Set source and destination directories
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    # Attach head to .annoation
    def attach(self):
        for filename in os.listdir(self.source):

            name = filename[:filename.index(".html")]
            html_path = os.path.join(self.source, filename)

            # Open, read .html file
            of = open(html_path)

            of_contents = of.read()

            # Pick <head> out of HTML
            h = re.search(r"<head[^>]*>(.*?)</head>", of_contents, re.DOTALL)
            head = h.group(1)
            head = "<head>\n" + head + "\n</head>"

            # Find appropriate (head-less) .annotation
            ann_path = name + u".annotation"

            if ann_path in os.listdir(self.dest):

                ann_file = os.path.join(self.dest, ann_path)

                # Open file
                fo = open(ann_file, "r")

                # Read annotated body from file
                body = fo.read()
                body = "<body>\n" + body + "\n</body>"

                # Close the file
                fo.close()

                # Delete it
                os.remove(ann_file)

                # Reopen it for writing
                fo = open(ann_file, "wb+")

                # Write head + annotation in .annotation
                fo.write(head)
                fo.write(body)

                # Close file again
                fo.close()

def usage():
    print """
    python headcrab.py <source_dir> <dest_dir>
    Read in list of source files, finds the appropriate
        .annotation in the destination folder, and prepends
        the head.
    """

# Run the data preparation
if __name__ == "__main__":

    if len(sys.argv)!=3:        # Expect exactly two arguments: the folder
        usage()                 # of annotated articles and output file name
        sys.exit(2)

    crabby = HeadCrab(sys.argv[1], sys.argv[2])
    crabby.attach()
