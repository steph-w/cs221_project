# k_means.py
# Determine paper topics by performing k-means on the text.

import os
import numpy as np
from sklearn import feature_extraction, cluster, preprocessing
from collections import OrderedDict
import operator
#  import seaborn as sns
import matplotlib.pyplot as plt

# import utilites
import imp
plotter = imp.load_source('plotter', '../utils/plotter.py')

CLUSTERS = 10

FILE_DIRECTORY = '../data/journal_ai_research_papers/split_by_article_clean/'
#  FILE_DIRECTORY = '../data/journal_ai_research_abstracts/papers_no_stopwords/'
#  TEST_FILE_DIRECTORY = 'test_data_clean/'

plt.close('all')
if True:

    files = []
    for r,ds,fs in os.walk(FILE_DIRECTORY):
        for f in fs:
            files.append(os.path.join(r, f))
    files = sorted(files)

    # Make feature vector
    vectorizer = feature_extraction.text.CountVectorizer(input="filename")
    vectorizer.fit(files)
    feature_names = vectorizer.get_feature_names()
    file_transform = vectorizer.transform(files)

    file_transform = preprocessing.normalize(file_transform)

    # Perform k-means
    kmeans = cluster.KMeans(n_clusters=10)
    kmeans.fit(file_transform)
    centers = kmeans.cluster_centers_
    prediction = kmeans.predict(file_transform)

    # Visulize results
    names = []
    for file in files:
        _, name = file.split(FILE_DIRECTORY)
        names.append(name)
    plt.figure(10)
    plt.grid(False)
    plotter.plot_trends_over_time_kmeans(prediction, range(len(names)))
    print prediction

    ## Get Categories for each Mean ##
    # Determine top words of each cluster
    #  cluster_top_words = {}
    #  for i in range(len(centers)):
        #  c = centers[i]
        #  max_indexes = np.argpartition(-c, len(c)-1)[:]
        #  max_words = [feature_names[index] for index in max_indexes]
        #  cluster_top_words[i] = set(max_words)

    #  for i, word_set in cluster_top_words.iteritems():
        #  print word_set



## Get Categories for each Mean ##
# Determine top words of each cluster
if True:
    NUM_TOP_WORDS = 10
    cluster_top_words = {}
    for i in range(len(centers)):
        c = centers[i]
        max_indexes = np.argpartition(c, -NUM_TOP_WORDS)[-NUM_TOP_WORDS:]
        max_indexes = max_indexes[np.argsort(c[max_indexes])]
        max_words = {feature_names[index]: c[index] for index in max_indexes}
        max_words = OrderedDict(sorted(max_words.items(), reverse=True, key=operator.itemgetter(1)))
        cluster_top_words[i] = max_words

    for i, word_dict in cluster_top_words.iteritems():
        labels =[k + '\n\n\n' for k,v in word_dict.iteritems()]
        print i
        print labels
        frequencies=[v for k,v in word_dict.iteritems()]
        plt.figure(i)
        plt.ylabel("Word frequency of this \"mean\"")
        plt.title("Top " + str(NUM_TOP_WORDS) + " words for Topic " + str(i))
        plt.bar(range(len(word_dict)),frequencies)
        plt.xticks(range(len(word_dict)), labels, rotation=30)
        plt.grid(True)
        plt.show(block=False)
        #  print word_dict



#perform prediction
#  test_files = sorted([os.path.join(TEST_FILE_DIRECTORY, f) for f in os.listdir(TEST_FILE_DIRECTORY)])
#  test_file_transform = vectorizer.transform(test_files)
#  test_prediction = kmeans.predict(test_file_transform)
#  print test_prediction

