# Latent Dirichlet Allocation Implementation, using Gibbs Sampling
from collections import OrderedDict
from pdb import set_trace as t
import numpy as np
import os, collections
import random
import sys

def read_data(data_directory):
    """
    data_directory: path to directory with all documents
    returns: dict of {document_name: text}
    """
    data = OrderedDict()  # Need to remember the order in which items were inserted
    for r, ds, fs in os.walk(data_directory):
        for f in sorted(fs):  # TODO Need to make sure inputs are in alphebetical order chronilogically
            fullpath = os.path.join(r, f)
            with open(fullpath, "r") as fr:
                lines = fr.read()
                data[f] = lines
        break
    return data

class LDA:
    def __init__(self, data):
        """
        data: dictor of {document_name: text}
        see http://u.cs.biu.ac.il/~89-680/darling-lda.pdf#page=7
        """
        print "Initializing LDA object."
        self.data = data
        self.corpus = [] # list of all words
        self.terms = [] # list of all unique words; i.e. the vocabulary
        self.doc_pointers = [] # list of document each word belongs to
        self.num_documents = len(data)

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
        self.terms = list(set(self.corpus))
        self.num_corpus_words = len(self.corpus)
        self.num_terms = len(self.terms)

    def run(self, num_topics, iterations=10, alpha_init=0.01, beta_init=0.01):
        """
        Another attempt, using: http://www.arbylon.net/publications/text-est.pdf#page=20

        """
        n_mk = np.zeros( (self.num_documents, num_topics), dtype=np.int )
        n_m = np.zeros( (self.num_documents), dtype=np.int )
        n_kt = np.zeros( (num_topics, self.num_terms), dtype=np.int )
        n_k = np.zeros( (num_topics), dtype=np.int )
        z = np.zeros( (self.num_documents, self.num_corpus_words), dtype=np.int )
        # TODO: these parameters could also be non-uniform
        alphas = np.full((num_topics), alpha_init)
        betas = np.full((self.num_terms), beta_init)

        # Converts index of self.corpus to index of self.terms
        def n_to_t(n):
            t = self.terms.index(self.corpus[n])
            return t

        # Initialization
        n = 0
        for m, doc_id in enumerate(self.data): # for each document
            while n < self.num_corpus_words and self.doc_pointers[n] == m:  # for each word in the doc
                # Sample random topic from multinomial
                dist = np.random.multinomial(1, [1./num_topics]*num_topics)
                k = np.where(dist==1)[0]
                # assign topic to word in document
                z[m, n] = k
                # increment counters based on assignment
                n_mk[m, k] += 1
                n_m[m] += 1
                n_kt[k, n_to_t(n)] += 1
                n_k[k] += 1
                # Move to next corpus word index
                n += 1

        # Gibbs sampling over burn-in period and sampling period
        for i in range(iterations):  # TODO could also check for convergence instead
            n = 0
            for m, doc_id in enumerate(self.data): # for each document
                while n < self.num_corpus_words and self.doc_pointers[n] == m:
                    # remove topic k from (doc m, word n) and decrement counters
                    k = z[m, n]
                    n_mk[m, k] -= 1
                    n_m[m] -= 1
                    n_kt[k, n_to_t(n)] -= 1
                    n_k[k] -= 1
                    # Multinomial sample using equation (79), note there is a typo
                    # There is a typo in this equation in the paper;
                    # t in the numerator of second fraction should be k, as below
                    probabilities = np.zeros( (num_topics) )
                    for topic in range(num_topics):
                        numerator1 = n_kt[topic,n_to_t(n)] * 1.0 + betas[n_to_t(n)]
                        denominator1 = sum(n_kt[topic, n_to_t(cur_n)] * 1.0 + betas[n_to_t(cur_n)] \
                                for cur_n in range(self.num_corpus_words))
                        numerator2 = n_mk[m,k] * 1.0 + alphas[k]
                        denominator2 = sum( n_mk[m, cur_k] * 1.0 + alphas[cur_k] \
                                for cur_k in range(num_topics)) - 1
                        probabilities[topic] = (numerator1 / denominator1) * (numerator2 / denominator2)
                    # normalize
                    p_total = sum(probabilities)
                    probabilities = [p / p_total for p in probabilities]
                    # sample from distribution
                    dist = np.random.multinomial(1, probabilities)
                    k = np.where(dist==1)[0]
                    # reassign counters based on sample
                    z[m,n] = k
                    n_mk[m,k] +=1
                    n_m[m] += 1
                    n_kt[k, n_to_t(n)] += 1
                    n_k[k] += 1
                    # increment corpus word index
                    n += 1
            print "Iteration %d complete" % (i+1)

        # read out phi, probability of a topic given a word
        # TODO: not using phi currently, but may be useful later
        for k in range(num_topics):
            denominator = sum(n_kt[k, topic] + betas[topic] for term in range(self.num_terms))
            for t in range(self.num_terms):
                phi_kt = (n_kt[k, t] + betas[t]) / denominator

        # read out theta, probability of a paper given a topic
        assignments = OrderedDict()
        for m, filename in enumerate(self.data):  # for each document
            denominator = sum(n_mk[m,cur_k] + alphas[cur_k] for cur_k in range(num_topics))
            theta_mks = np.zeros(num_topics)
            for k in range(num_topics):
                theta_mk = (n_mk[m,k] + alphas[k]) / denominator
                theta_mks[k] = theta_mk
            assignments[filename] = np.argmax(theta_mks) # Just taking max probability

        return assignments


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
    data = read_data("../data/trivial/")
    lda = LDA(data)
    lda.generate_corpus()
    assignments = lda.run(num_topics=3, iterations=10, alpha_init=0.01, beta_init=0.01)
    print
    print "ASSIGNMENTS: "
    for k in assignments:
        print k, ":", assignments[k]
    print

