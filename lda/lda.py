# Latent Dirichlet Allocation Implementation, using Gibbs Sampling
import os, collections
import random
from pdb import set_trace as t
import numpy as np
import sys

ROOT = '../'
DATA_DIRECTORY = os.path.join(ROOT, "data/simple/")

def read_data(data_directory):
    """
    data_directory: path to directory with all documents
    returns: dict of {document_name: text}
    """
    data = {}
    for r, ds, fs in os.walk(DATA_DIRECTORY):
        for f in fs:
            fullpath = os.path.join(r, f)
            with open(fullpath, "r") as fr:
                lines = fr.read()
                data[f] = lines
        break
    return data

# Function: Weighted Random Choice
# --------------------------------
# Given a dictionary of the form element -> weight, selects an element
# randomly based on distribution proportional to the weights. Weights can sum
# up to be more than 1.
def weightedRandomChoice(weightDict):
    weights = []
    elems = []
    for elem in weightDict:
        weights.append(weightDict[elem])
        elems.append(elem)
    total = sum(weights)
    key = random.uniform(0, total)
    runningTotal = 0.0
    chosenIndex = None
    for i in range(len(weights)):
        weight = weights[i]
        runningTotal += weight
        if runningTotal > key:
            chosenIndex = i
            return elems[chosenIndex]
    raise Exception('Should not reach here')

class LDA:
    def __init__(self, data):
        """
        data: dictor of {document_name: text}
        see http://u.cs.biu.ac.il/~89-680/darling-lda.pdf#page=7
        """
        print "Initializing LDA object."
        self.data = data
        self.num_iterations = 1
        self.corpus = [] # list of all words, length N
        self.doc_pointers = [] # list of document each word belongs to, length N
        self.num_topics = 3 # K
        self.num_documents = len(data)
        # TODO don't know what these superparameters should be
        self.alpha = 0.5
        self.beta = 0.5

    def generate_corpus(self):
        """
        creates the corpus from given data
        """
        print "Generating corpus."
        for doc_id, doc in enumerate(self.data):
            text = self.data[doc]
            for word in text.split():
                self.corpus.append(word)
                self.doc_pointers.append(doc_id)
        self.num_corpus_words = len(self.corpus)

    def run2(self):
        """
        Another attempt, using: http://www.arbylon.net/publications/text-est.pdf#page=20

        """
        n_mk = np.zeros( (self.num_documents, self.num_topics), dtype=np.int ) #size?
        n_m = np.zeros( (self.num_documents), dtype=np.int )
        n_kt = np.zeros( (self.num_topics, self.num_corpus_words), dtype=np.int )
        n_k = np.zeros( (self.num_topics), dtype=np.int )
        z = np.zeros( (self.num_documents, self.num_corpus_words), dtype=np.int )

        alphas = np.full( (self.num_topics), 0 )
        betas = np.full( (self.num_corpus_words), 0 )


        # initialization
        n = 0
        for m, doc_id in enumerate(self.data): # for each document
            while n < self.num_corpus_words and self.doc_pointers[n] == m:  # for each word in the doc
                # Sample random topic from multinomial
                dist = np.random.multinomial(1, [1./self.num_topics]*self.num_topics)
                k = np.where(dist==1)[0]
                # assign topic to word in document
                z[m, n] = k
                # increment counters based on assignment
                n_mk[m, k] += 1
                n_m[m] += 1
                n_kt[k, n] += 1
                n_k[k] += 1

                n += 1

        # Gibbs sampling over burn-in period and sampling period
        i = 0
        while True:
            n = 0
            for m, doc_id in enumerate(self.data): # for each document
                while n < self.num_corpus_words and self.doc_pointers[n] == m:
                    # decrement word
                    k = z[m, n]
                    n_mk[m, k] -= 1
                    n_m[m] -= 1
                    n_kt[k, n] -= 1
                    n_k[k] -= 1

                    # Multinomial sample
                    probabilities = np.zeros( (self.num_topics) )
                    for topic in range(self.num_topics):
                        numerator1 = n_kt[topic,n] * 1.0 + betas[n]

                        denominator1 = sum(n_kt[topic, cur_n] * 1.0 + betas[cur_n] \
                                for cur_n in range(self.num_corpus_words))


                        print m
                        print n
                        print topic
                        numerator2 = n_mk[m,n] * 1.0 + alphas[topic]

                        denominator2 = sum( n_mk[m, cur_k] * 1.0 + alphas[cur_k] \
                                for cur_k in range(self.num_topics)) - 1

                        #  print numerator1, denominator1, numerator2, denominator2

                        probabilities[topic] = (numerator1 / denominator1) * (numerator2 / denominator2)
                        print probabilities

                    #  print probabilities
                    #  print np.sum(probabilities)
                    dist = np.random.multinomial(1, [1./self.num_topics]*self.num_topics)
                    k = np.where(dist==1)[0]

                    # TODO: maybe not using correct variables for t
                    z[m,n] = k
                    n_mk[m,k] +=1
                    n_m[m] += 1
                    n_kt[k, n] += 1
                    n_k[k] += 1

                    n += 1

            if True and i >= self.num_iterations:
                # read out phi
                # read out theta
                break
            i += 1


    def get_topics(self, assignments, n_dk):
        """
        Returns a dict of {}

        """
        print "Retrieving results."
        topics = collections.defaultdict(list)
        for i in range(len(self.corpus)):
            topics[assignments[i]].append(self.corpus[i])
        assigns = {}
        for row_index in range(len(n_dk)):
            assigns[row_index] = np.argmax(n_dk[row_index])
        return topics, assigns

if __name__ == "__main__":
    print
    data = read_data(DATA_DIRECTORY)
    lda = LDA(data)
    lda.generate_corpus()
    # lda.generate_document_corpus()
    lda.run2()
    #  topics, assigns = lda.get_topics(assignments, n_dk)
    print "done."
    print

