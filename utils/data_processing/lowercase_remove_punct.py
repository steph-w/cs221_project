import os
import re
import string


INPUT_DIR = "test_data/"
OUTPUT_DIR = "output/"

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

for r,ds,fs in os.walk(INPUT_DIR):
    for f in fs:
        with open(os.path.join(r,f), "r") as fr:
            lines = fr.readlines()
        output_file = os.path.join(OUTPUT_DIR, f)

        with open(output_file, "w") as fw:
            for line in lines:
                line = line.lower()
                line = ''.join(ch for ch in line if ch not in set(string.punctuation))
                fw.write(line)
        print "wrote contents of: "  + output_file
