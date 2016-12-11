# Cleans up abstracts, leaving only authors, title, and text

import os
import re
import string


ABSTRACT_DIR = "abstracts_raw/"
OUTPUT_DIR = "output/"

header_re = r'(?<=<cite>).*?(?=</cite>)'
#  content_re = r'(?<=\<p\>).*?(?=</p>)|(?<=\<p\>).*|.*(?=</p>)'

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

numheaders = 0
for r,ds,fs in os.walk(ABSTRACT_DIR):
    for f in fs:
        with open(os.path.join(r,f), "r") as fr:
            lines = fr.readlines()
        output_file = os.path.join(OUTPUT_DIR, f)
        output_file = output_file.replace(" ", "_")
        with open(output_file, "w") as fw:
            first = True
            for line in lines:
                header_search = re.search(header_re, line)
                #  content_search = re.search(content_re, line)
                if header_search:
                    numheaders += 1
                    to_write = header_search.group(0).decode("ascii", "ignore")
                    if not first:
                        fw.write("\n\n\n")
                    first = False
                    to_write = ''.join(ch for ch in to_write if ch not in set(string.punctuation))
                    to_write = to_write.lower()
                    fw.write(to_write + "\n" + "\n")
                if "<p>" in line or "</p>" in line and not "</a>" in line:
                    to_write = line.decode("ascii", "ignore")
                    to_write = to_write.strip().replace("<br />", "").replace("<p>", "").replace("</p>", "")
                    to_write = ''.join(ch for ch in to_write if ch not in set(string.punctuation))
                    to_write = to_write.lower()
                    fw.write(to_write + "\n")
        print "wrote contents of: "  + output_file


print "headers: %d" % numheaders
