import re
import urllib3
import os

# Contants.
root = "http://www.jair.org"
url = "http://www.jair.org/contents.html"
output_dir = "./PDFS"

# Get data.
pool = urllib3.PoolManager()
r = pool.request('GET', url)
lines = r.data.split("\n")


#  print "Getting links to Volume pages"
#  volume_page_links = {}
#  for line in lines:
    #  volume_link_re = r"(?<=href=\")[^\"]*"
    #  volume_name_re = r"(?<=html\">)[^\n]*"
    #  if "Volume " in line:
        #  link_match = re.search(volume_link_re, line)
        #  name_match = re.search(volume_name_re, line)
        #  if link_match and name_match:
            #  link_suffix = link_match.group(0)
            #  link_cleaned = os.path.join(root, link_suffix)
            #  name_dirty = name_match.group(0)
            #  name_cleaned = name_dirty.replace("</a>", "").replace("</li>", "")
            #  volume_page_links[name_cleaned] = link_cleaned
        #  else:
            #  print "VOLUME PAGE RE ERROR"


#  print "Getting links to pdf pages"
#  abstract_links = {}
#  for volname, link in volume_page_links.iteritems():
    #  lines = pool.request('GET', link).data.split("\n")
    #  cur_abstract_links = []
    #  for line in lines:
        #  if "Abstract" in line:
            #  abstract_link_re = r"(?<=href=\")[^\"]*(?=\">PDF)"
            #  match = re.search(abstract_link_re, line)
            #  if match:
                #  abstract_link_suffix = match.group(0)
                #  abstract_link = root + abstract_link_suffix
                #  cur_abstract_links.append(abstract_link)
    #  abstract_links[volname] = cur_abstract_links

print "Downloading abstract lines"
abstract_text = {}
for volname, links in abstract_links.iteritems():
    text = []
    i = 0
    volname = volname.strip()
    if not os.path.exists(volname):
        os.mkdir(volname)
    else:
        continue
    for link in links:
        r = pool.request('GET', link, preload_content=False)
        pdfname = os.path.join(volname, str(i) + ".pdf")
        with open(pdfname, 'wb') as fr:
            print "Writing: " + pdfname
            while True:
                data = r.read(8)
                if not data:
                    break
                fr.write(data)
        i += 1



