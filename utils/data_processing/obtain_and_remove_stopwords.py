import os
import re
import collections
from nltk.corpus import stopwords
'''
remove words that occur more than M/10 times in the corpus, 
where M is the number of documents.

remove words that occur less than 3 times in the corpus
'''
# Step 1 obtain stopwords
IF = './just_letters'
corpus = []
for r,ds,fs in os.walk(IF):
	for f in fs:
		text = []
		with open(os.path.join(r,f), 'r') as fr:
			text = fr.readlines()
		#print "gathering term frequency: " + f
		for line in text:
			for word in line.split():
				corpus.append(word)

c = collections.Counter(corpus)
upper_threshold = 9*57
stop_words = []
for word in list(c):
	if c[word] > upper_threshold:
		stop_words.append(word)
		del c[word]
	elif c[word] <= 5:
		stop_words.append(word)
		del c[word]
# Step 2 remove stopwords

IF = './just_letters'
OF = './split_by_article_clean'
CUSTOM_WORDS = set(stop_words)
cachedStopWords = set(stopwords.words("english"))
cachedStopWords.update(CUSTOM_WORDS)
cachedStopWords.update(('the', 'if', 'this', 'but', 'in', 'at', 'that', 
	'by', 'these', 'we', 'as', 'also', 'like', 'fi', 'ff', 
	'problem', 'problems', 'volume', 'algorithm', 'pages', 'planning', 'show',
	'paper', 'results', 'publish', 'research', 'result', 'results', 'find', 
	'algorithms', 'based', 'models', 'approach', 'using', 'new', 'either', 'various', 'wellknown',
	'always'))

if not os.path.exists(OF):
	os.mkdir(OF)

for r,ds,fs in os.walk(IF):
	for f in fs:
		text = []
		with open(os.path.join(r,f), 'r') as fr:
			text = fr.readlines()
		#print "removing stop words: " + f
		goodtext = [' '.join(filter(lambda x: x.lower() not in cachedStopWords, line.split())) + '\n' for line in text]
		of_path_name = os.path.join(OF,os.path.basename(r))

		if not os.path.exists(of_path_name):
			os.mkdir(of_path_name)

		f_name = re.sub('.txt', '', f)
		of_name = os.path.join(of_path_name, f_name)
		with open(of_name,'w') as fw:
			fw.writelines(goodtext)
print cachedStopWords


