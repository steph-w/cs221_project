import os
import re
import collections

IF = './split_by_paper'
corpus = []
for r,ds,fs in os.walk(IF):
    for f in fs:
        text = []
        with open(os.path.join(r,f), 'r') as fr:
            text = fr.readlines()
        print "gathering term frequency: " + f
        for line in text:
            for word in line.split():
                corpus.append(word)

c = collections.Counter(corpus)
print c