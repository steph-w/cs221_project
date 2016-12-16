import os
import shutil
import string
from subprocess import call

IF = 'pdfs'
OF = 'text'


if os.path.exists(OF):
    shutil.rmtree(OF)
os.mkdir(OF)
for r,ds,fs in os.walk(IF):
    f_int = 0
    for f in fs:
        if not ".pdf" in f:
            continue
        justname, _ = f.split(".pdf")
        if f_int < 10:
            name = "0" + str(f_int) + ".txt"
        else:
            name = str(f_int) + ".txt"
        of_name = os.path.join(r, name).replace(IF, OF)
        if not os.path.exists(os.path.dirname(of_name)):
            os.mkdir(os.path.dirname(of_name))
        call(["pdftotext", os.path.join(r,f), of_name])
        print "    finished: " + f
        f_int += 1
    "Directory: " + r + " complete"


# clean unicode
for r, ds, fs in os.walk(OF):
    for f in fs:
        text = []
        with open(os.path.join(r,f), "r") as fr:
            text = fr.readlines()
        print "cleaning: " + f
        filter_func = lambda x: x in set(string.printable)
        goodtext = [filter(filter_func, line) for line in text]

        unicode_func = lambda x: x.replace(u'\x0c', 'fi').replace(u'\x0b', 'ff')
        goodtext = [unicode_func(line) for line in goodtext]

        with open(os.path.join(r,f), 'w') as fw:
            fw.writelines(goodtext)
