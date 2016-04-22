import os
import sys
import json
import re
from nltk.corpus import stopwords
from math import *
from nltk.stem import WordNetLemmatizer
from collections import *

DATA = sys.argv[3]

def vwfriendly(w):
    return w.replace(":", "COLON").replace("|", "PIPE")

def loadEmodict():
    ans = {}
    with open(os.path.join(DATA, "emodict.txt"), "r") as f:
        for line in f:
            fields = line.rstrip("\n").split("\t")
            ans[fields[0]] = [word.decode("utf-8") for word in fields[1].split(" ")]
    return ans

def loadPosNeg():
    pos = set()
    with open(os.path.join(DATA, "positive-words.txt"), "r") as f:
        for line in f:
            pos.add(line.rstrip("\n"))
    neg = set()
    with open(os.path.join(DATA, "negative-words.txt"), "r") as f:
        for line in f:
            neg.add(line.rstrip("\n"))
    return pos, neg

def loadBrown():
    brown = {}
    with open(os.path.join(DATA, "brown-clusters.txt"), "r") as f:
        for line in f:
            fields = line.rstrip("\n").split("\t")
            brown[fields[1]] = fields[0]
    return brown

def loadBrownDict():
    brown = {}
    with open(os.path.join(DATA, "brown-dict.txt"), "r") as f:
        for line in f:
            fields = line.rstrip("\n").split("\t")
            for w in fields[1].split(" "):
                brown[w] = fields[0]
    return brown

def removeDupChar(word):
    ans = ""
    for i, w in enumerate(word):
        if (i >= 2 and w == word[i - 1] and w == word[i - 2]):
            continue
        ans += w
    return ans

def normalizeText(text):
    ans = []
    for word in text:
        if (word.startswith("@")):
            word = "USERNAME"
        if (url_regex.match(word)):
            word = "URL"
        if (num_regex.match(word)):
            word = "NUMBER"
        for key in emodict:
            if (word in emodict[key]):
                word = key
                break
        word = word.replace(":", "COLON").replace("|", "PIPE")
        if (not word in keywords):
            word = word.lower()
        word = removeDupChar(word)
        ans.append(word.encode("utf-8"))
    return ans


def extractFeatures(text, tags):
    longexpress = 0
    for word in text:
        nword = removeDupChar(word)
        if (nword != ".."):
            longexpress += nword != word

    text = normalizeText(text)
    ans = []
    cntPos = cntNeg = 0
    cntTags = defaultdict(int)
    brown_str = []

    ans.append("LONGEXPRESS_" + str(longexpress))
    for i, word in enumerate(text):
        ans.append(word)
        ans.append(word + "_" + text[i - 1])
        cntPos += word in pos
        cntNeg += word in neg
        cntTags[tags[i]] += 1
        if (word in brown):
            brown_str.append(brown[word])
    brown_str = sorted(brown_str, key = lambda e : len(e))
    cntBrownPrefix = {}
    for i, prefix in enumerate(brown_str):
        prefix = prefix[:-1]
        cntBrownPrefix[prefix] = 0
        for code in brown_str[i:]:
            if (code.startswith(prefix)):
                cntBrownPrefix[prefix] += 1
    for prefix, cnt in cntBrownPrefix.iteritems():
        ans.append("Brown_" + prefix + ":" + str(cnt))
    ans.append("cntPos" + str(cntPos))
    ans.append("cntNeg" + str(cntNeg))
    for tag in pos_tags:
        ans.append("cntTag_" + tag + ":" + str(round(cntTags[tag] * 1.0 / len(text), 2)))

    return " ".join(ans)

"""def oaa():
    with open(os.path.join(DATA, "tweets.vw." + out + "." + inp), "w") as w:
        for inst in data:
            print >> w, labelmap[inst["sentiment"]], "| " + extractFeatures(inst["tweet"], inst["pos"])
            """

def csoaa():
    cost = defaultdict(lambda : defaultdict(float))
    cost[1][3] = cost[3][1] = cost[2][1] = cost[2][3] = 1
    cost[1][2] = cost[3][2] = 1
    with open(os.path.join(DATA, "tweets.vw." + out + "." + inp), "w") as w:
        for inst in data:
            label = labelmap[inst["sentiment"]]
            for pred in xrange(1, 4):
                print >> w, str(pred) + ":" + str(cost[label][pred]), 
            print >> w, "| " + extractFeatures(inst["tweet"], inst["pos"])


url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
num_regex = re.compile(r'^[0-9]+[.,]*[0-9]$')
keywords = ["COLON", "USERNAME","URL","COLON", "PIPE", "NUMBER"]
pos_tags = ["N", "O", "S", "^", "Z", "L", "M", "V", "A", "R", "!", "D", "P", "&", "T", "X", "Y", "#", "@", "~", "U", "E", "$", ",", "G"]


emodict = loadEmodict()
for key in emodict:
    keywords.append(key)

pos, neg = loadPosNeg()
brown = loadBrown()
#brown_dict = loadBrownDict()

inp = sys.argv[1]
with open(os.path.join(DATA, "tweets.tok." + inp), "r") as f:
    data = json.load(f)

labelmap = {}
labelmap["positive"] = 3
labelmap["neutral"] = 2
labelmap["negative"] = 1

out = sys.argv[2]

csoaa()
    


