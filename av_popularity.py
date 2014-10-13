# -*- coding: utf-8 -*-
import os
import spelunky_lb
from datetime import date
from spelunky_lb import avatars

# - Requires ~60MB memory
# ALL DAILIES FROM RELEASE TO DATE:
#   Fetching via requests:
#   - Takes ~8 minutes on my Chromebook
#   Locally cached XML:
#   - Takes ~5 minutes on my Chromebook
# ONE MONTH (November, 2013):
#   Fetching via requests:
#   - Takes ~2 minutes on my Chromebook
#   Locally cached XML:
#   - Takes ~50 seconds on my Chromebook
# TODO:
# - Append entries past 5000 into tree before working with rows (prototype in get_pages.py)

since = date(2013, 11, 1)
until = date(2013, 11, 30)
# since = None
# until = None

av_tally = {a: 0 for a in avatars}
dailies = spelunky_lb.dailies(since=since, until=until, force=True)

for d in dailies:
    with d as lb:
        for r in lb:
            av_tally[r.avatar] += 1
        print "done with %s" % lb.date

av_sort = sorted(av_tally.items(), key=lambda x:x[1], reverse=True)

with open(os.path.join('output', 'avatars.txt'), 'w') as outfile:
    for c in av_sort:
        print "%s\t%i" % c
        outfile.write("%s\t%i\n" % c)
