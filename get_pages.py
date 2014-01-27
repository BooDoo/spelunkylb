import xml.etree.ElementTree as etree
import requests
import os
import sys

def get_pages(url, page=0, label=None, persist=True, infile=None,
              force=False, max_page=sys.maxint):
    trees = []
    while True:
        tree = get_page(url, page, label, persist, infile, force)
        trees.append(tree)
        next_url = tree.findtext('nextRequestURL')
        if page >= max_page or not next_url:
            break
        else:
            url = next_url
            page += 1
    return trees

def get_page(url, page=0, label=None, persist=True, infile=None, force=False):
    print "Getting %s" % url
    label = label or url.split('/')[-2]
    infile = infile or os.path.join('data', '%s-%02d.xml' % (label, page))
    if force or not os.path.exists(infile):
        r = requests.get(url)
        tree = etree.fromstring(r.content)
        if persist:
            print "Writing to %s..." % infile
            with open(infile, 'w') as outfile:
                outfile.write(etree.tostring(tree))
    else:
        tree = etree.parse(infile)
    return tree

# e.g. to get all pages of the "High Scores" leaderboard:
# get_pages('http://steamcommunity.com/stats/239350/leaderboards/164848/?xml=1',label='high_scores')
