import sys
import os

inp = sys.argv[1]
idmap = ["negative", "neutral", "positive"]
pred = []
with open(inp, "r") as f:
    for line in f:
        predid = int(line.rstrip("\n")) - 1
        pred.append(idmap[predid])

original = sys.argv[2]
with open(original + ".pred", "w") as w:
    with open(original, "r") as f:
        for i, line in enumerate(f):
            fields = line.rstrip("\n").split("\t")
            fields[2] = pred[i]
            print >> w, "\t".join(fields)


