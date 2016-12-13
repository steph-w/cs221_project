import os
from nltk.corpus import stopwords

IF = './clean'
OF = './clean_no_stopwords'
CUSTOM_WORDS = ('the', 'if', 'this', 'but', 'in', 'at', 'that', 'by', 'these', 'we', 'as')
cachedStopWords = set(stopwords.words("english"))
cachedStopWords.update(CUSTOM_WORDS)

if not os.path.exists(OF):
	os.mkdir(OF)

for r,ds,fs in os.walk(IF):
	for f in fs:

		text = []
		with open(os.path.join(r,f), 'r') as fr:
			text = fr.readlines()
		print "removing stop words: " + f
		goodtext = [' '.join(filter(lambda x: x.lower() not in cachedStopWords, line.split())) + '\n' for line in text]
		of_name = os.path.join(OF, f)
		with open(of_name, 'w') as fw:
			fw.writelines(goodtext)

