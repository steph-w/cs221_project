import re
import urllib3
import os

# Contants.
root = "http://www.jair.org"
url = "http://www.jair.org/contents.html"
output_dir = "./abstracts"

# Get data.
pool = urllib3.PoolManager()
r = pool.request('GET', url)
lines = r.data.split("\n")


print "Getting links to Volume pages"
volume_page_links = {}
for line in lines:
    volume_link_re = r"(?<=href=\")[^\"]*"
    volume_name_re = r"(?<=html\">)[^\n]*"
    if "Volume " in line:
        link_match = re.search(volume_link_re, line)
        name_match = re.search(volume_name_re, line)
        if link_match and name_match:
            link_suffix = link_match.group(0)
            link_cleaned = os.path.join(root, link_suffix)
            name_dirty = name_match.group(0)
            name_cleaned = name_dirty.replace("</a>", "").replace("</li>", "")
            volume_page_links[name_cleaned] = link_cleaned
        else:
            print "VOLUME PAGE RE ERROR"


print "Getting links to abstract pages"
abstract_links = {}
for volname, link in volume_page_links.iteritems():
    lines = pool.request('GET', link).data.split("\n")
    cur_abstract_links = []
    for line in lines:
        if "Abstract" in line:
            abstract_link_re = r"(?<=href=\")[^\"]*(?=\">Abstract)"
            match = re.search(abstract_link_re, line)
            if match:
                abstract_link_suffix = match.group(0)
                abstract_link = root + abstract_link_suffix
                cur_abstract_links.append(abstract_link)
    abstract_links[volname] = cur_abstract_links

print "Downloading abstract lines"
abstract_text = {}
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
for volname, links in abstract_links.iteritems():
    #  yes = True
    #  for word in ["51:", "21:", "17:", "33:", "12:", "52:", "46:", "43:", "10:", "13:", "11:", "42:", "50:", "28:", "36:", "53:", "41:", "37:", "49:", "47:", "19:", " 5:", " 7:", " 9:", "38:", "31:", "56:", "30:", "29:", "20:", "26:", " 1:", " 2:", "32:", "39:", "44:", "54:", " 6:", " 3:", "48:", "16:"]:
        #  if word in volname:
            #  yes = False
    #  if not yes:
        #  continue
    text = []
    for link in links:
        abstract_lines = pool.request('GET', link).data.split("\n")
        on = False
        for line in abstract_lines:
            if not on:
                if "class=\"abstract\"" in  line:
                    on = True
                continue
            if on and "</div" in line:
                on = False
                continue
            text.append(line)
        text.append("")
    print "Writing: " + volname
    with open(os.path.join(output_dir, volname), 'w') as fw:
        fw.write("\n".join(text))



