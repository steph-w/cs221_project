# removes all non-printable characters from pdf file output
import os
import string
import unicodedata
from unidecode import unidecode

IF = 'txt-dirty'
OF = 'txt-clean'

if not os.path.exists(OF):
    os.mkdir(OF)

for r, ds, fs in os.walk(IF):
    for f in fs:

        text = []
        with open(os.path.join(r,f), "r") as fr:
            text = fr.readlines()
        print "cleaning: " + f
        filter_func = lambda x: x in set(string.printable)
        goodtext = [filter(filter_func, line) for line in text]

        unicode_func = lambda x: x.replace(u'\x0c', 'fi').replace(u'\x0b', 'ff')
        goodtext = [unicode_func(line) for line in goodtext]

        of_name = os.path.join(r, f).replace(IF, OF)
        with open(of_name, 'w') as fw:
            fw.writelines(goodtext)
