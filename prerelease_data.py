# -*- coding: utf-8 -*-

import spelunky_lb


lbs = spelunky_lb.leaderboards()
prerelease = (lb for lb in lbs if lb.entries > 0 
              and lb.entries < 25 and lb.name.endswith("DAILY"))
output = open('output/prerelease.txt', 'w')

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
