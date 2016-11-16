# Latent Dirichlet Allocation Implementation, using Gibbs Sampling
import os, collections
import random
from pdb import set_trace as t

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
        self.num_iterations = 1
        self.corpus = [] # list of all words, length N
        self.doc_pointers = [] # list of document each word belongs to, length N
        self.num_topics = 5 # K
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
        n_dk = [[1 for i in range(len(data))] for j in range(self.num_topics)]
        n_kw = [[1 for i in range(self.num_topics)] for j in range(len(self.corpus))]
        n_k =  [1 for i in range(self.num_topics)]
        for ii in range(self.num_iterations):
            for jj in range(len(self.corpus)):
                weights = collections.defaultdict(float)
                word = self.corpus[jj]
                doc = self.doc_pointers[jj]
                topic = assignments[jj]
                n_dk[topic][doc] -= 1
                n_kw[jj][topic] -=1
                n_k[topic] -= 1
                for kk in range(self.num_topics):
                    # TODO: Check this weight assignment
                    weights[topic] = (n_dk[kk][doc]+self.alpha)*((n_kw[jj][kk]+self.beta)/(n_k[kk]+self.beta))
                topic = weightedRandomChoice(weights)
                assignments[jj] = topic
                n_dk[topic][doc] +=1
                n_kw[jj][topic] += 1
                n_k[topic] += 1
        return assignments, n_dk, n_kw, n_k
if __name__ == "__main__":
    print
    data = read_data(DATA_DIRECTORY)
    lda = LDA(data)
    lda.generate_corpus()
    # lda.generate_document_corpus()
    topics = lda.run()
    print "done."
    print
    #  lda.get_topics()

