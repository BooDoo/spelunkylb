import spelunky_lb
# As of Jan 26, 2014:
# - This took ~10 minutes on my Chromebook over wifi
# - If you leave the persist() call, data/* will be ~100MB
# - output/all.txt will be a ~25MB "human readable" txt file

#TODO:
# - Sort dailies by date first!
# - Append entries past 5000 into tree before working with rows

lbs = spelunky_lb.leaderboards()
dailies = (lb for lb in lbs if lb.name.endswith('DAILY'))

output = open('output/all.txt', 'w')

for lb in dailies:
    lb.persist()
    print lb.date
    output.write(str(lb.date)+"\n"+("-"*10)+"\n")
    #print "-"*10
    for row in lb:
        #print row
        output.write(str(row)+"\n")
    #print "-"*50,"\n"
    output.write(("-"*50)+"\n\n")

output.close()
