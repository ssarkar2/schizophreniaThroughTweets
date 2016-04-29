#http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
import nltk

'''
def rhyme(inp, level): #if level is higher, it returns more strictly matched rhymes. level must e integer
    inp = inp.lower()
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)


def doTheyRhyme (word1, word2, level):
    return word1 in rhyme (word2, level)
'''

def getOverlap(seq1, seq2, region): 
    t = len(seq1)
    maxMatchLen = 0.; currMatchLen = 0.; matchIdx = -100;
    for i in xrange(0, t):
        if seq1[i] == seq2[i]:
            currMatchLen += 1.
            if currMatchLen > maxMatchLen:
                maxMatchLen = currMatchLen; matchIdx = i #matchIdx is the location where the best match ends
        else:
            currMatchLen = 0.

    addExtra = 0.
    if region == 2 and matchIdx == t-1:  #the match is at the end of the words
        addExtra = (0.6,1)[maxMatchLen > 1]  #if its a good quality match at the end of the word (>=2 syllable match), add +1, else all +0.6
    if region == 1 and matchIdx == maxMatchLen-1:  #the match is at the beginning of the words
        addExtra = 0.3
    return maxMatchLen + addExtra

    

def longestSyllablesMatch(syl1, syl2): #convolution/cross-correlation like implementation. assume syl1 is fixed and syl2 'moves' around
    #syl1, syl2 are list of syllables (string)
    if len(syl2) > len(syl1):  #ensure that syl2 is the shorter list
        t = syl2; syl2 = syl1; syl1 = t;
    l1 = len(syl1); l2 = len(syl2)
    maxMatch = 0
    #The number of possible alignments is l1+l2-1. dividing into 3 parts 'entering' overlap, full overlap and 'exit' overlap
    #'entry' overlap. head of syl1 and tail of syl2
    for overlapLen in xrange(1, l2):
        t = getOverlap(syl1[0:overlapLen], syl2[-overlapLen:], 0)
        #print syl1[0:overlapLen], syl2[-overlapLen:], 0, l2-overlapLen, t
        if t > maxMatch: maxMatch = t

    #full overlap
    for idx in xrange(0, l1-l2):
        t = getOverlap(syl1[idx:idx+l2], syl2, (1,0)[idx!=0])
        #print syl1[idx:idx+l2], syl2, idx, 0, t
        if t > maxMatch: maxMatch = t

    #'exit' overlap. tail of syl1 and head of syl2
    for overlapLen in xrange(l2,0,-1):
        t = getOverlap(syl1[-overlapLen:], syl2[0:overlapLen], (2,0)[overlapLen!=l2])
        #print syl1[-overlapLen:], syl2[0:overlapLen], l1-overlapLen, 0, t
        if t > maxMatch: maxMatch = t

    return maxMatch/(1,l1+l2)[(l1+l2)>0]


def getWordSyllableDict():
    return {entry[0]:entry[1] for entry in nltk.corpus.cmudict.entries()}

def getRhymingScoreForText(textList, entries):  #are punctuations, newline etc cleaned up before coming here?  #longer texts will have lesser rhyming pairs.
    textSplitList = [[i.lower() for i in text.split(' ')] for text in textList]
    retval = []
    for textSplit in textSplitList:
        ln = len(textSplit)
        sylList = [entries.get(word, []) for word in textSplit]
        scorelist = []
        for idx1 in xrange(0,ln-1):
            for idx2 in xrange(idx1+1, ln):
                #print textSplit[idx1], textSplit[idx2]
                scorelist += [longestSyllablesMatch(sylList[idx1], sylList[idx2])]
        retval += [scorelist]
    return retval



'''
#print doTheyRhyme('clang', 'bang', 2)
#print rhyme('Bang', 1)

entries = getWordSyllableDict()

inp = 'goes'
syllables = entries.get('goes', [])
print syllables

print 'xxxxxxxxx'
#print entries.get('clang', []), entries.get('bang', [])
print longestSyllablesMatch(entries.get('bang', []), entries.get('clang', []))
#print longestSyllablesMatch([], [])
#print entries.get('hello', []), entries.get('world', [])
print longestSyllablesMatch(entries.get('hello', []), entries.get('world', []))

tweet = ['clang bang here there fsfdfd', 'hello world']
print getRhymingScoreForText(tweet, entries)  #[[0.42857142857142855, 0, 0, 0, 0, 0, 0, 0.26666666666666666, 0, 0], [0.125]]
'''


