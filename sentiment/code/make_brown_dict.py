
brown = {}
with open("../../data/semeval2015/brown-clusters.txt", "r") as f:
    for line in f:
        fields = line.rstrip("\n").split("\t")
        if (not fields[0] in brown):
            brown[fields[0]] = []
        brown[fields[0]].append((fields[1], int(fields[2])))

dictmap = {}
for k, v in brown.iteritems():
    wordpairs = sorted(v, key=lambda e : -e[1])
    if (wordpairs[0][1] <= 500):
        continue
    origin = wordpairs[0][0]
    dictmap[origin] = []
    for w, c in wordpairs:
        if (w != origin and c <= 50):
            dictmap[origin].append(w)

with open("../../data/semeval2015/brown-dict.txt", "w") as w:
    for k, v in dictmap.iteritems():
        print >> w, k + "\t" + " ".join(v)
    
        
