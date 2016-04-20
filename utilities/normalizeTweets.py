from utilities.ark_tweet_nlp_0_3_2.ark_tweet_nlp_python.CMUTweetTagger import *
import pickle
import os

def normTweet1(tweets):
    tokenizedTweets = tokenizeCMUPython(tweets)
    tweet2EngWordPairs = gettweet2EngWordPairsDict()
    dictKeys = tweet2EngWordPairs.keys()
    for tokenizedTweet in tokenizedTweets:
        for wordIdx in xrange(len(tokenizedTweet)):
            word = tokenizedTweet[wordIdx]
            if word[0] in dictKeys:
                tokenizedTweet[wordIdx] = (tweet2EngWordPairs[word[0]], word[1], word[2]);
    return [tokenizedTweets, joinBackTokens(tokenizedTweets)]


def joinBackTokens(tokenizedTweets):
    return [ (' ').join([word[0] for word in tweet]) for tweet in tokenizedTweets]

    


def gettweet2EngWordPairsDict():
    picklePath = 'utilities/tweet2EngWordPairs.pickle'
    textPath = 'utilities/tweet2EngWordPairs.txt'
    if os.path.isfile(picklePath):
        with open(picklePath, 'r') as f:
            tweet2EngWordPairs = pickle.load(f)
    else:
        t = [line.split('\t')[1].split('|') for line in open(textPath, 'r').read().split('\n') if line != '']
        tweet2EngWordPairs = {i[0].strip():i[1].strip() for i in t}
        with open(picklePath, 'w') as fp:
            pickle.dump(tweet2EngWordPairs, fp)
    return tweet2EngWordPairs


def tokenizeCMUPython(tweets):
    RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar utilities/ark_tweet_nlp_0_3_2/ark-tweet-nlp-0.3.2.jar"
    print "Checking that we can see \"%s\", this will crash if we can't" % (RUN_TAGGER_CMD)
    success = check_script_is_present(RUN_TAGGER_CMD)
    if success:
        print "Tokenizing..."
        return runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD)
