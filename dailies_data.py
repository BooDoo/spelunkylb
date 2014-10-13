#!/usr/bin/env python2

import spelunky_lb
import datetime
# As of Jan 26, 2014:
# PRERELEASE DATES ONLY:
#   Fetching via requests:
#   - ~1 minute on my Chromebook
#   Locally cached XML:
#   - <10 seconds on my Chromebook
# RECORDS FROM RELEASE TO DATE:
# ! If you persist locally (default) call, data/* will be ~100MB
# - output/dailies.txt will be a ~27MB "human readable" txt file
#   Fetching via requests:
#   - ~10m:30s on my Chromebook
#   Locally cached XML:
#   - ~5m:45s on my Chromebook
#
# TODO:
# - Append entries past 5000 into tree before working with rows (prototype in get_pages.py)

## All dailies
# since = None # Defaults to release date
# until = datetime.date.today()

## Prerelease-only dates (for smaller tables/dataset)
# since = datetime.date(2013, 5, 30)
# until = datetime.date(2013, 8, 7)

## Test uncached:
since = datetime.date(2014, 10, 12)
until = datetime.date.today()

dailies = spelunky_lb.dailies(sort=True, persist=True, since=since, until=until)

output = open('output/dailies.txt', 'w')
for d in dailies:
    with d as lb:
        lb.persist();
        print lb.date
        output.write(str(lb.date)+"\n"+("-"*10)+"\n")
        for row in lb:
            output.write(str(row)+"\n")
        output.write(("-"*50)+"\n\n")
output.close()
