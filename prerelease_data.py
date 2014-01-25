# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
from spelunky_lb import avatars, Leaderboard
from spelunky_lb import LbRow as Row

lbs = etree.parse('leaderboards.xml').getroot().iter('leaderboard')
prerelease = (Leaderboard(lb) for lb in lbs if int(lb[4].text) > 0 
              and int(lb[4].text) < 25 and lb[2].text.endswith("DAILY"))
output = open('prerelease.txt', 'w')

for lb in prerelease:
    #print "Persisting data..."
    #lb.persist(outpath='data/'+lb.lbid+'.xml')
    print lb.date
    output.write(str(lb.date)+"\n"+("-"*10)+"\n")
    print "-"*10
    for row in lb:
        print row
        output.write(str(row)+"\n")
    print "-"*50,"\n"
    output.write(("-"*50)+"\n\n")

output.close()
