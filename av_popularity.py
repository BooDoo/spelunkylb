# -*- coding: utf-8 -*-
import os
import sys
import spelunky_lb
from datetime import date
from spelunky_lb import avatars
from itertools import chain

# - Only reads ranks 1-5000 of each daily
# - Requires ~60MB memory
# TIMING:
#   Downloading/tallying all Dailies via requests:
#   - Takes ~8 minutes on my Chromebook
#   Tallying locally cached XML for all Dailies:
#   - Takes ~5 minutes on my Chromebook
#   Tallying one month (November 2013) locally cached XML:
#   - Takes ~50 seconds on my Chromebook

since = date(2013, 11, 1)
until = date(2013, 11, 30)
since = None
until = None

av_tally = {a: 0 for a in avatars}
dailies = spelunky_lb.dailies(since=since, until=until)

for d in dailies:
    with d as lb:
        for r in lb:
            av_tally[r.avatar] += 1
        print "done with %s" % lb.date
        
av_tally = {a: 0 for a in avatars}

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
