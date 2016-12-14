import os
import re
import collections
'''
remove words that occur more than M/10 times in the corpus, 
where M is the number of documents.

remove words that occur less than 3 times in the corpus
'''
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
upper_threshold = (13*57)/10
print upper_threshold
stop_words = []
for word in list(c):
	if c[word] > upper_threshold:
		stop_words.append(word)
		del c[word]
	elif c[word] < 3:
		stop_words.append(word)
		del c[word]
print stop_words, c, upper_threshold



