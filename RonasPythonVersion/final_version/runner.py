import sys
from clust import clust
from dataprep import dataprep
from clustering import clustering


class Runner(object):
    def main(self):
        # Parse input
        exists_load_context = False
        load_context = ""
        exists_save_context = False
        save_context = ""
        segsize = 10000
        outfile = ""
        root_path = ""
        list_file = ""
        major_threshold = -1
        minor_threshold = -1

        for i in range(1, len(sys.argv), 2):
            tag = sys.argv[i]
            param = sys.argv[i + 1]
            if tag == '-l':
                exists_load_context = True
                load_context = param
            elif tag == '-s':
                exists_save_context = True
                save_context = param
            elif tag == '-i':
                seg_size = int(param)
            elif tag == '-r':
                root_path = param
            elif tag == '-f':
                list_file = param
            elif tag == '-T':
                major_threshold = float(param)
            elif tag == '-t':
                minor_threshold = float(param)
            else:
                print 'Unknown Tag: ', tag
        error = False
        if root_path == "":
            error = True
            print "Missing mandatory param: root_dir"
        if list_file == "":
            error = True
            print "Missing mandatory param: list_file"
        if major_threshold > 1 or major_threshold < 0:
            error = True
            print "Invalid major threshold given - [0, 1]"
        if minor_threshold > 1 or minor_threshold < 0:
            error = True
            print "Invalid minor threshold given - [0, 1]"
        if error:
            sys.exit()

        # Get tfidfs
        dp = dataprep(root_path, list_file)
        dp.data_prep()

        # Do clustering
        c = clustering(load_context, save_context, segsize, list_file,
                       major_threshold, minor_threshold)
        c.cluster()

if __name__ == u'__main__':
    Runner().main()
