# Latent Dirichlet Allocation Implementation, using Gibbs Sampling
from collections import OrderedDict
from pdb import set_trace as t
import numpy as np
import os, collections
import random
import sys
import pyLDAvis
import json

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
    def __init__(self, data, num_topics, alpha_init=0.01, beta_init=0.01):
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

        self.generate_corpus()

        self.n_mk = np.zeros( (self.num_documents, num_topics), dtype=np.int )
        self.n_m = np.zeros( (self.num_documents), dtype=np.int )
        self.n_kt = np.zeros( (num_topics, self.num_terms), dtype=np.int )
        self.n_k = np.zeros( (num_topics), dtype=np.int )
        self.z = np.zeros( (self.num_documents, self.num_corpus_words), dtype=np.int )
        # TODO: these parameters could also be non-uniform
        self.alphas = np.full((num_topics), alpha_init)
        self.betas = np.full((self.num_terms), beta_init)
        self.beta_init = beta_init
        self.num_topics = num_topics

        self.phi_kt = np.zeros((self.num_topics, self.num_terms), dtype = np.float)
        self.theta_mk = np.zeros((self.num_documents, self.num_topics), dtype = np.float)

        # Initialization
        print "Initializing."
        n = 0
        for m, doc_id in enumerate(self.data): # for each document
            while n < self.num_corpus_words and self.doc_pointers[n] == m:  # for each word in the doc
                # Sample random topic from multinomial
                dist = np.random.multinomial(1, [1./self.num_topics]*self.num_topics)
                k = np.where(dist==1)[0]
                # assign topic to word in document
                self.z[m, n] = k
                # increment counters based on assignment
                self.n_mk[m, k] += 1
                self.n_m[m] += 1
                self.n_kt[k, self.n_to_t(n)] += 1
                self.n_k[k] += 1
                # Move to next corpus word index
                n += 1

    # Converts index of self.corpus to index of self.terms
    def n_to_t(self, n):
        t = self.terms.index(self.corpus[n])
        return t

    def generate_corpus(self):
        """
        creates the corpus from given data
        """
        print "Generating corpus."
        self.doc_lengths = np.zeros((self.num_documents), dtype=np.int)
        for doc_id, doc in enumerate(self.data):
            text = self.data[doc]
            for word in text.split():
                self.corpus.append(word)
                self.doc_pointers.append(doc_id)
                self.doc_lengths[doc_id] += 1
        c = collections.Counter(self.corpus)
        self.term_freq = [cnt for elem, cnt in c.items()]
        self.terms = [elem for elem, cnt in c.items()]
        self.num_corpus_words = len(self.corpus)
        self.num_terms = len(self.terms)

    def inference(self, iterations=10):
        """
        Another attempt, using: http://www.arbylon.net/publications/text-est.pdf#page=20

        """
        print "Inference"
        # Gibbs sampling over burn-in period and sampling period
        for i in range(iterations):  # TODO could also check for convergence instead
            n = 0
            for m, doc_id in enumerate(self.data): # for each document
                while n < self.num_corpus_words and self.doc_pointers[n] == m:
                    # remove topic k from (doc m, word n) and decrement counters
                    k = self.z[m, n]
                    self.n_mk[m, k] -= 1
                    self.n_m[m] -= 1
                    self.n_kt[k, self.n_to_t(n)] -= 1
                    self.n_k[k] -= 1
                    # Multinomial sample using equation (79), note there is a typo
                    # There is a typo in this equation in the paper;
                    # t in the numerator of second fraction should be k, as below
                    probabilities = np.zeros( (self.num_topics) )
                    for topic in range(self.num_topics):
                        numerator1 = self.n_kt[topic, self.n_to_t(n)] * 1.0 + self.betas[self.n_to_t(n)]
                        denominator1 = self.n_k[topic] + self.beta_init
                        numerator2 = self.n_mk[m,k] * 1.0 + self.alphas[k]
                        denominator2 = sum( self.n_mk[m, cur_k] * 1.0 + self.alphas[cur_k] \
                                for cur_k in range(self.num_topics)) - 1
                        probabilities[topic] = (numerator1 / denominator1) * (numerator2 / denominator2)
                    # normalize
                    p_total = sum(probabilities)
                    probabilities = [p / p_total for p in probabilities]
                    # sample from distribution
                    dist = np.random.multinomial(1, probabilities)
                    k = np.where(dist==1)[0]
                    # reassign counters based on sample
                    self.z[m,n] = k
                    self.n_mk[m,k] +=1
                    self.n_m[m] += 1
                    self.n_kt[k, self.n_to_t(n)] += 1
                    self.n_k[k] += 1
                    # increment corpus word index
                    n += 1
            print "Iteration %d complete" % (i+1)

    def output_paper_topic_dist(self):
        # read out phi, probability of a topic given a word
        # used to compute the perplexity of LDA with changing parameters
        for k in range(self.num_topics):
            denominator = sum(self.n_kt[k, term] + self.betas[term] for term in range(self.num_terms))
            for t in range(self.num_terms):
                self.phi_kt[k, t] = (self.n_kt[k, t] + self.betas[t]) / denominator

        # read out theta, probability of a paper given a topic
        assignments = OrderedDict()
        
        for m, doc_id in enumerate(self.data):
            denominator = sum(self.n_mk[m, k] + self.alphas[k] for k in range(self.num_topics))
            for k in range(self.num_topics):
                self.theta_mk[m, k] = (self.n_mk[m, k] + self.alphas[k]) / denominator

        for m, doc_id in enumerate(self.data):
            assignments[doc_id] = np.argmax(self.theta_mk[m])

        return assignments

    def perplexity(self):
        """
        Returns the perplexity of the model, lower the better
        Used for tuning the number of topics, alpha and beta
        see http://qpleple.com/perplexity-to-evaluate-topic-models/

        """
        log_per = 0
        docs_len = 0
        for m, doc_id in enumerate(self.data): # for each document
            likelihood = 0
            for t in range(self.num_terms): # for each term 
                # num times term t appears in doc m
                n_mt = sum([1 for n in range(self.num_corpus_words) if self.doc_pointers[n]==m and self.n_to_t(n)==t]) 
                inner_product = 0
                for k in range(self.num_topics):
                    inner_product += np.inner(self.phi_kt[k, t], self.theta_mk[m, k])
                likelihood += n_mt * np.log(inner_product)
                docs_len += n_mt
            log_per -= likelihood
        return np.exp(log_per / docs_len)

    def launch_visualization(self):
        """
        Creates an interactive visual in the browser
        See https://github.com/bmabey/pyLDAvis for installation and usage

        """
        data = { 'topic_term_dists': self.phi_kt,
        'doc_topic_dists': self.theta_mk,
        'doc_lengths': self.doc_lengths,
        'vocab': self.terms,
        'term_frequency': self.term_freq}
        vis_data = pyLDAvis.prepare(**data)
        pyLDAvis.show(vis_data)

if __name__ == "__main__":
    print
    data = read_data("../data/journal_ai_research_abstracts/cleaned/")
    lda = LDA(data, num_topics=20, alpha_init=4, beta_init=0.01)
    lda.inference(iterations=20)
    assignments = lda.output_paper_topic_dist()
    print 
    #print "Model perplexity %f" % (lda.perplexity())
    target = open('output.txt', 'w')
    print
    print "ASSIGNMENTS: "
    for k in assignments:
        print k, ":", assignments[k]
        target.write(str(assignments[k]))
        target.write('\n')
    target.close()
    print
    lda.launch_visualization()
    


