import os
from subprocess import call

for r,ds,fs in os.walk('./'):
    for f in fs:
        if not ".pdf" in f:
            continue
        justname, _ = f.split(".")
        f_int = int(justname)
        if f_int < 10:
            name = "0" + justname + ".txt"
        call(["pdftotext", os.path.join(r,f), os.path.join(r, name)])
        print "    finished: " + f
    "Directory: " + r + " complete"

