# Latent Dirichlet Allocation Implementation, using Gibbs Sampling
import os
from random import randint

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
        self.num_topics = 5 # K
        # TODO don't know what these superparameters should be
        self.alpha = 0.5
        self.beta = 0.5

    def generate_corpus(self):
        """
        creates the corpus from given data
        """
        print "Generating corpus."
        corpus = set()
        for _, text in self.data.iteritems():
            for word in text.split():
                corpus.add(word)
        self.corpus = list(corpus)

    def run(self):
        """
        returns: dict of {document_name: [topics]}
        """
        print "Performing LDA. (not implemented)"
        # TODO: are all below these initialized correctly?
        assignments = [randint(0,self.num_topics) for i in range(len(self.corpus))] # z
        # n_dk[d][k] = number of words from doc d assigned to topic k
        # n_kw[k][w] = number of times word w is assigned to topic k
        # n_k = number of times any word assigned to topic k
        n_dk = [[1 for i in range(len(data))] for j in range(self.num_topics)]
        n_kw = [[1 for i in range(self.num_topics)] for j in range(len(self.corpus))]
        n_k =  [1 for i in range(self.num_topics)]

        for ii in range(self.num_iterations):
            for jj in range(len(self.corpus)):
                pass





if __name__ == "__main__":
    print
    data = read_data(DATA_DIRECTORY)
    lda = LDA(data)
    lda.generate_corpus()
    topics = lda.run()
    print "done."
    print
    #  lda.get_topics()

