import os
import re
from nltk.corpus import stopwords

IF = './split_by_paper'
OF = './papers_no_stopwords'
CUSTOM_WORDS = ('the', 'if', 'this', 'but', 'in', 'at', 'that', 
	'by', 'these', 'we', 'as', 'also', 'like', 'fi', 'ff', 
	'problem', 'problems', 'volume', 'algorithm', 'pages', 'planning', 'show',
	'paper', 'results', 'publish', 'research', 'result', 'results', 'find', 
	'algorithms', 'based', 'models', 'approach', 'using', 'new', 'programs', 'program')
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
		of_path_name = os.path.join(OF,os.path.basename(r))

		if not os.path.exists(of_path_name):
			os.mkdir(of_path_name)
		f_name = re.sub('.txt', '', f)
		of_name = os.path.join(of_path_name, f_name)
		with open(of_name,'w') as fw:
			fw.writelines(goodtext)