# Latent Dirichlet Allocation Implementation, using Gibbs Sampling
import os, collections
import random
from pdb import set_trace as t
import numpy as np

ROOT = '../'
DATA_DIRECTORY = os.path.join(ROOT, "data/journal_ai_research_abstracts/cleaned/")

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
        self.num_iterations = 5
        self.corpus = [] # list of all words, length N
        self.doc_pointers = [] # list of document each word belongs to, length N
        self.num_topics = 7 # K
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

    def run(self):
        """
        returns: dict of {document_name: [topics]}
        """
        print "Performing LDA. (not implemented)"
        # TODO: are all below these initialized correctly?
        assignments = [random.randint(0,self.num_topics-1) for i in range(len(self.corpus))] # z
        # n_dk[k][d] = number of words from doc d assigned to topic k
        # n_kw[w][k] = number of times word w is assigned to topic k
        # n_k = number of times any word assigned to topic k
        # initialize
        n_dk = np.zeros((len(data), self.num_topics))
        n_kw = np.zeros((self.num_topics, len(self.corpus)))
        n_k = np.zeros(self.num_topics)

        for i, w in enumerate(self.corpus):
            topic = np.random.randint(self.num_topics)
            doc = self.doc_pointers[i]
            n_dk[doc, topic] += 1
            n_kw[topic, i] += 1
            n_k[topic] += 1

        for ii in range(self.num_iterations):
            for jj in range(len(self.corpus)):
                word = self.corpus[jj]
                doc = self.doc_pointers[jj]
                topic = assignments[jj]
                n_dk[doc, topic] -= 1
                n_kw[topic, jj] -=1
                n_k[topic] -= 1

                left = (n_dk[doc, :]+self.alpha)
                right = (n_kw[:,jj]+self.beta)/(n_k+self.beta)
                topic_weights = left * right
                weights = {i: weight for i, weight in enumerate(topic_weights)}

                topic = weightedRandomChoice(weights)
                assignments[jj] = topic
                n_dk[doc, topic] +=1
                n_kw[topic, jj] += 1
                n_k[topic] += 1
        return assignments, n_dk, n_kw, n_k


        self.assignments = assignments
        self.n_dk = n_dk
        self.n_kw = n_kw
        self.n_k = n_k

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
    assignments, n_dk, n_kw, n_k = lda.run()
    topics, assigns = lda.get_topics(assignments, n_dk)
    print "done."
    print

