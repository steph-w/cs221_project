# Removes non-letters and converts to lowercase

import os
import re
import shutil
import string

IF = './articles_no_stopwords'
OF = './just_letters'

if os.path.exists(OF):
    shutil.rmtree(OF)
shutil.copytree(IF, OF)


for r,ds,fs in os.walk(OF):
    for f in fs:
        with open(os.path.join(r,f), 'r') as fr:
            text = fr.read()
        clean_text = re.sub(r'[^a-zA-Z\n\r ]', " ", text)
        clean_text = clean_text.lower()
        with open(os.path.join(r,f), 'w') as fw:
            fw.write(clean_text)
        print "wrote file: " + f

