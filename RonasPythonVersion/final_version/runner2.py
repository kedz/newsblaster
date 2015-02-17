from cluster import Cluster
import os

def main():
    input_type = "file_path"
    seg_size = 10000
    maj_threshold = 0.2
    min_threshold = 0.5
    c = Cluster(input_type, seg_size, maj_threshold, min_threshold)
    documents = sorted(os.listdir('../pres_root_dir_1/documents'))
    for i in range(0, len(documents)):
        documents[i] = os.path.join('../pres_root_dir_1/documents', documents[i])
    labels = c.fit(documents)
    results = c.predict([documents[0], documents[3], documents[19]])
    print results

if __name__ == u'__main__':
    main()
