import re, collections, pickle, os

#http://norvig.com/spell-correct.html

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    #def f(): return 1
    model = {} #collections.defaultdict()  #removimg lambda x:1 as default val, as pickle cant dump lambda functions
    for f in features:
        #model[f] += 1
        model[f] = model.get(f,0) + 1
    return model

def edits1(word):
   alphabet = 'abcdefghijklmnopqrstuvwxyz'
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word, NWORDS):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words, NWORDS): return set(w for w in words if w in NWORDS)

def correct(word):  #single word correction
    if os.path.isfile('utilities/NWORDS.pickle'):
        with open('utilities/NWORDS.pickle') as f:
            NWORDS = pickle.load(f)
    else:
        NWORDS = train(words(file('utilities/big.txt').read()))
        with open('utilities/NWORDS.pickle', 'w') as f:
            pickle.dump(NWORDS, f)
    word = word.lower()
    candidates = known([word], NWORDS) or known(edits1(word), NWORDS) or known_edits2(word, NWORDS) or [word]
    #return max(candidates, key=NWORDS.get)
    return max(candidates, key=lambda k : NWORDS.get(k,1))


def spellCorrectTokenizedTweets(TokenizedTweets, ignoreTags, threshold):
    if os.path.isfile('utilities/NWORDS.pickle'):
        with open('utilities/NWORDS.pickle') as f:
            NWORDS = pickle.load(f)
    else:
        NWORDS = train(words(file('utilities/big.txt').read()))
        with open('utilities/NWORDS.pickle', 'w') as f:
            pickle.dump(NWORDS, f)

    correctedTokenisedTweets = []
    for tokenizedTweet in TokenizedTweets:
        correctedTokenisedTweet = []
        for wordIdx in xrange(len(tokenizedTweet)):
            word = tokenizedTweet[wordIdx]  #its a tuple as defined by khanh (word, tag, prob)
            if (word[1] not in ignoreTags  and (word[2] > threshold)) or ((word[1] in ignoreTags and word[2] < threshold)):
                wordtxt = word[0].lower()
                candidates = known([wordtxt], NWORDS) or known(edits1(wordtxt), NWORDS) or known_edits2(wordtxt, NWORDS) or [wordtxt]
                #correctedTokenisedTweet += [(max(candidates, key=NWORDS.get), word[1], word[2])]
                correctedTokenisedTweet += [(max(candidates, key=lambda k : NWORDS.get(k,1)), word[1], word[2])]
            else:
                correctedTokenisedTweet += [word]
        correctedTokenisedTweets += [correctedTokenisedTweet]
    return correctedTokenisedTweets


#print correct('spellng')
#print correct('Wrld')



