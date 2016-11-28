# k_means.py
# Determine paper topics by performing k-means on the text.

import os
import numpy as np
from sklearn import feature_extraction, cluster

FILE_DIRECTORY = '../data/trivial/'
TEST_FILE_DIRECTORY = 'test_data_clean/'


files = sorted([os.path.join(FILE_DIRECTORY, f) for f in os.listdir(FILE_DIRECTORY)])

# Make feature vector
vectorizer = feature_extraction.text.CountVectorizer(input="filename")
vectorizer.fit(files)
feature_names = vectorizer.get_feature_names()
file_transform = vectorizer.transform(files)

# Perform k-means
kmeans = cluster.KMeans(n_clusters=3)
kmeans.fit(file_transform)
centers = kmeans.cluster_centers_
prediction = kmeans.predict(file_transform)

# Visulize results
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
NUM_TOP_WORDS = 1
cluster_top_words = {}
for i in range(len(centers)):
    c = centers[i]
    max_indexes = np.argpartition(-c, NUM_TOP_WORDS)[:NUM_TOP_WORDS]
    max_words = [feature_names[index] for index in max_indexes]
    cluster_top_words[i] = set(max_words)
# Keep only top words unique to that particular cluster
unique_cluster_top_words = {}
for i, word_set in cluster_top_words.iteritems():
    set_of_rest = set()
    for j, word_set2 in cluster_top_words.iteritems():
        if i == j:
            continue
        set_of_rest.update(word_set2)
    unique_cluster_top_words[i] = word_set.difference(set_of_rest)
# Remove words that have <=5 characters or contain digits
unique_cluster_top_words_filtered = {}
for i, word_set in unique_cluster_top_words.iteritems():
    new_set = set()
    for word in word_set:
        if len(word) > 0 and not any(c.isdigit() for c in word):
            new_set.add(word)
    unique_cluster_top_words_filtered[i] = new_set

for i, word_set in unique_cluster_top_words_filtered.iteritems():
    print word_set



#perform prediction
#  test_files = sorted([os.path.join(TEST_FILE_DIRECTORY, f) for f in os.listdir(TEST_FILE_DIRECTORY)])
#  test_file_transform = vectorizer.transform(test_files)
#  test_prediction = kmeans.predict(test_file_transform)
#  print test_prediction

