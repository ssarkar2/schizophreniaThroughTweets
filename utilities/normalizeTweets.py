from utilities.ark_tweet_nlp_0_3_2.ark_tweet_nlp_python.CMUTweetTagger import *
import pickle
import os

def normTweet1(tweets):
    tokenizedTweets = tokenizeCMUPython(tweets)
    d1 = getTweet2EngWordPairsDict(1); d2 = getTweet2EngWordPairsDict(1);
    d1.update(d2)  #join the 2 dictionaries. note if a certain key is present in both, dict1's value will override dict0's value in this line
    dictKeys = d1.keys()
    for tokenizedTweet in tokenizedTweets:
        for wordIdx in xrange(len(tokenizedTweet)):
            word = tokenizedTweet[wordIdx]
            if word[0] in dictKeys:
                tokenizedTweet[wordIdx] = (d1[word[0]], word[1], word[2]);
    return [tokenizedTweets, joinBackTokens(tokenizedTweets)]


def joinBackTokens(tokenizedTweets):
    return [ (' ').join([word[0] for word in tweet]) for tweet in tokenizedTweets]

    


def getTweet2EngWordPairsDict(dictNum):
    picklePath = ['utilities/tweet2EngWordPairs1.pickle', 'utilities/tweet2EngWordPairs2.pickle']
    textPath = ['utilities/tweet2EngWordPairs.txt', 'utilities/emnlp_dict.txt']
    if os.path.isfile(picklePath[dictNum]):
        with open(picklePath[dictNum], 'r') as f:
            tweet2EngWordPairs = pickle.load(f)
    else:
        if dictNum == 0:
            t = [line.split('\t')[1].split('|') for line in open(textPath[dictNum], 'r').read().split('\n') if line != '']
        if dictNum == 1:
            t = [line.split(('\t', ' ')[' ' in line]) for line in open(textPath[dictNum], 'r').read().split('\n') if line != '']  #split on '\t' or ' ' depending on which is present
        tweet2EngWordPairs = {i[0].strip():i[1].strip() for i in t}
        with open(picklePath[dictNum], 'w') as fp:
            pickle.dump(tweet2EngWordPairs, fp)
    return tweet2EngWordPairs


def tokenizeCMUPython(tweets):
    RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar utilities/ark_tweet_nlp_0_3_2/ark-tweet-nlp-0.3.2.jar"
    print "Checking that we can see \"%s\", this will crash if we can't" % (RUN_TAGGER_CMD)
    success = check_script_is_present(RUN_TAGGER_CMD)
    if success:
        print "Tokenizing..."
        return runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD)
