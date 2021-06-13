import scipy.spatial.distance
import scipy.cluster.hierarchy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import json
import string
from matplotlib import pyplot as plt
import numpy as np


def find_files(loc):
    file_list = []
    slice = len(loc)
    for root, dirs, files in os.walk(loc):
        for file in files:
            if file.endswith(".json"):
                file_list.append(os.path.join(root, file))
    return file_list

def list_text(files):
    texts = []
    for file in files:
        with open(file, "r") as read_file:
            data = json.load(read_file)
            texts.append(data["content"])
    return texts


def text_prep(documents):
    new_docs = []
    for doc in documents:
        stop_words = set(stopwords.words('english'))
        period_space = doc.translate(str.maketrans('.', ' '))
        no_punc = period_space.translate(str.maketrans('', '', string.punctuation))
        word_tokens = word_tokenize(no_punc)
        filtered_sentence = [w.lower() + " " for w in word_tokens if not w.lower() in stop_words]
        new_docs.append("".join(filtered_sentence))
    return new_docs


def vectorize(documents):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(documents)
    return vectorizer.transform(documents)

def score(term_matrix):
    return linear_kernel(term_matrix)

#For preparing: remove stop words and stem

# For representation: bag of words??

#For distance scoring: cosine similarity

#for clustering: hierarch-agglo slink or clink

def cluster_indices(cluster_assignments):
    n = cluster_assignments.max()
    indices = []
    for cluster_number in range(1, int(n) + 1):
        indices.append(np.where(cluster_assignments == cluster_number)[0])
    return indices

def run_clustering(file_location):
    files = find_files(file_location)
    texts = list_text(files)
    texts = text_prep(texts)
    vector = vectorize(texts)
    scores = score(vector)
    pdist = scipy.spatial.distance.pdist(scores)
    Z = scipy.cluster.hierarchy.linkage(pdist, method="complete")
    print(pdist)
    print(Z)
    fig = plt.figure(figsize=(10, 8))
    dn = scipy.cluster.hierarchy.dendrogram(Z, color_threshold=0.6*max(Z[:,2]))
    num_clusters = Z.max()
    print("%d clusters" % num_clusters)
    indices = cluster_indices(Z)
    height = max([i[2] for i in Z])
    print(height)
    # for k, ind in enumerate(indices):
    #     print("cluster", k + 1, "is", ind)
    # clusters = [(height, scipy.cluster.hierarchy.fcluster(Z, height, criterion='distance')) for height in [(n*(2.5/20)) for n in range(12)]]
    clusters = [(1.0, scipy.cluster.hierarchy.fcluster(Z, Z.max()/3, criterion='maxclust'))]
    print(clusters)
    file_names = [[],[]]
    for i in range(len(clusters)):
        print(clusters[i][0])
        print(clusters[i][1])
        file_names[0].append(clusters[i][0])
        temp = [(clusters[i][1][k], files[k][len(file_location):]) for k in range(len(clusters[i][1]))]
        temp = sorted(temp, key=lambda s: s[0])
        print(temp)
        file_names[1].append([(clusters[i][1][k], files[k]) for k in range(len(clusters[i][1]))])

    # plt.show()

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')
    run_clustering("C:\\Users\\Daniel O'Reilly\\PycharmProjects\\CPSC_473_Project\\news_data")