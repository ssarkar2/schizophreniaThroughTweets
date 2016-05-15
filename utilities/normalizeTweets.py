from utilities.ark_tweet_nlp_0_3_2.ark_tweet_nlp_python.CMUTweetTagger import *
from utilities.spellChecker import spellCorrectTokenizedTweets
from utilities.wordSeparator import parseTagSingleWordFast, InitializeWords, parseTagSingleWord
import pickle
import os, timeit

'''
description of normTweet1 usage
normTweet1 takes tweetList as input...which is a list of tweet strings
It tokenizes them using tokenizeCMUPython

getSpecialTokens is called next. it divides the tokens in the tweets by token types
eg: from tokenizer we got: [[('#helloBye', '#', 0.9), ('there', 'D', 0.9)], [('an', 'D', 0.9), (':)', 'E', 0.9), ('#spelingMistake', '#', 0.9)], [('Wrld', 'N', 0.9)]]
Then getSpecialTokens(tokenizedTweets, f, ops, ['#', 'E'], retain = 0) will return:
separatedByTokenType = [[hashtags] , [emoticons] , [rest of the things without hashtags or emoticons]]   Note if retain was 1, then the 3rd sublist would have retained the hashtags and emoticons
expanding separatedByTokenType explicitly, it looks like: [[[('hello bye', '#', 0.765)], [('spe ling mistake', '#', 0.8214)], []], [[], [(':)', 'E', 0.9852)], []], [[('there', 'R', 0.5307)], [('an', 'D', 0.7642)], [('Wrld', 'N', 0.3949)]]]
So what happens here is that the words in the hashtags are separated out and placed in the first sublist (per tweet basis).Then emoticons (per tweet basis) are placed in second bin and the rest of the stuff in the 3rd bin. Note if there are no # in a tweet, then that entry of the 1st bin is empty
eg separatedByTokenType[0][2] is empty, as the tweet#2 does not have any hashtags

Finally spellcheck and clean up is performed on separatedByTokenType[-1]

separatedByTokenType and joinBackTokens(separatedByTokenType[-1]) is returned. joinBackTokens 'untokenizes' the tokens, that is joins things up and makes a list of strings, where each string is a cleaned tweet
separatedByTokenType after spellcheck is: [[[('hello bye', '#', 0.765)], [('spe ling mistake', '#', 0.8214)], []],    [[], [(':)', 'E', 0.9852)], []],    [[('#helloBye', '#', 0.765), ('there', 'R', 0.5307)], [('an', 'D', 0.7642), (':)', 'E', 0.9852), ('#spelingMistake', '#', 0.8214)], [('world', '^', 0.3878), ('world', '^', 0.4131)]]]
joinBackTokens gives: ['#helloBye there', 'an :) #spelingMistake', 'world world']
'''

#in retain = 0, the last bin does not retain any token in separateTokens
#in retain = 1, the last bin retains unprocessed token in separateTokens
#in retain = 2, the last bin does not retain token in separateTokens. It splits and retains '#' in last bin though
def normTweet1(tweets, ops = [0,1], retain = 1, separateTokens = ['#', 'E']): 
    ignoreTags = ['E', ',', 'U', '&', '^', '!', '#']   #do not do anything if its a emoticon or punctuation or URL('U') or hashtag('#') or or abbreviations like lol ('!')
    threshold = 0.7  #only clean words to which high confidence POS is given. This stops the cleaner from replacing '@' with 'a' etc
    tokenizedTweets = tokenizeCMUPython(tweets)
    #print 'tokenizeCMUPython done'
    f = [wordReplace, spellCorrectTokenizedTweets]

    #start = timeit.default_timer()
    if os.path.isfile('utilities/wordseparator.pickle'):
        with open('utilities/wordseparator.pickle') as fl:
            wordlist = pickle.load(fl)
    else:
        wordlisttxt = 'utilities/englishWords.txt' # A file containing common english words  #assumes we are running from the top directory (schizophreniaThroughTweets)
        wordlist = InitializeWords(wordlisttxt)
        with open('utilities/wordseparator.pickle', 'w') as fl:
            pickle.dump(wordlist, fl)
    #print 'got wordlist', timeit.default_timer() - start

    #separatedByTokenType has 3 parts say, eg: [hashtagsInTweetsText, emoticonInTweetsText, restInTweetsText]
    separatedByTokenType = getSpecialTokens(tokenizedTweets, f, ops, wordlist, separateTokens, retain)  #get hashtags and emoticons out of each tweet.     #retain=1 argument makes the last bin retain the tokenTypes that are already separated out in the first bins
    
    #do cleaning/spell check in last element of separatedByTokenType (which contains the bulk of the words)
    for op in ops:
        separatedByTokenType[-1] = f[op](separatedByTokenType[-1], ignoreTags, threshold)  #wordReplace(tokenizedTweets, ignoreTags, threshold) and spellCorrectTokenizedTweets(tokenizedTweets, ignoreTags, threshold)
    return [separatedByTokenType, joinBackTokens(separatedByTokenType[-1])]
    

def getSpecialTokens(tokenizedTweets, funcs, ops, wordlist, tokenTypes = ['#', 'E'], retain = 0):  #retain=1 argument makes the last bin retain the tokenTypes that are already separated out in the first bins
    retval = [[[] for j in xrange(0, len(tokenizedTweets))] for i in xrange(0,len(tokenTypes)+1)]  #extra 1 for the 'not present in tokenTypes'     
    #c=0    
    for tokenizedTweetIdx in xrange(0, len(tokenizedTweets)):
        #c+=1
        #if c%100 == 0:
        #    print c, len(tokenizedTweets), 'xx',
        for word in tokenizedTweets[tokenizedTweetIdx]:
            #start = timeit.default_timer()
            flag = 0
            try:
                idx = tokenTypes.index(word[1])
            except:
                idx = len(tokenTypes) #the last slot is the catch-all slot
                flag = 1
            #separate out hashtag
            if (word[1] == '#' and '#' in tokenTypes) or  (retain == 2 and word[1] == '#'):  #the hashtag is separated out and processed by calling parseTagSingleWord() if word[1] is '#   #if retain == 2, then we retain the '#', but process it.
                t = (parseTagSingleWordFast(word[0], wordlist), word[1], word[2])
                #t = (parseTagSingleWord(word[0]), word[1], word[2])
            else:
                t = word

            if retain == 1 and flag == 0:
                retval[len(tokenTypes)][tokenizedTweetIdx].append(word)  #if retain == 1, then we retain the unprocessed '#'
            if retain == 2 and flag == 0:
                if word[1] == '#':
                    retval[len(tokenTypes)][tokenizedTweetIdx].append(t)
                #else:
                #    retval[len(tokenTypes)][tokenizedTweetIdx].append(word)
            retval[idx][tokenizedTweetIdx].append(t)
            #if word[1] == '#':
            #    print 'processed word', word[0], c, timeit.default_timer() - start
    return retval


def wordReplace(tokenizedTweets, ignoreTags, threshold):
    print 'in wordreplace'
    if os.path.isfile('utilities/wordreplace.pickle'):
        with open('utilities/wordreplace.pickle') as f:
            d1 = pickle.load(f)
    else:
        d1 = getTweet2EngWordPairsDict(1); d2 = getTweet2EngWordPairsDict(0);
        d1.update(d2)  #join the 2 dictionaries. note if a certain key is present in both, dict1's value will override dict0's value in this line
        with open('utilities/wordreplace.pickle', 'w') as f:
            pickle.dump(d1, f)
    
    #d1 = getTweet2EngWordPairsDict(1); d2 = getTweet2EngWordPairsDict(0);
    #d1.update(d2)  #join the 2 dictionaries. note if a certain key is present in both, dict1's value will override dict0's value in this line
    dictKeys = d1.keys()
    #c = 0
    for tokenizedTweet in tokenizedTweets:
        #c+=1
        #if c%100 == 0:
        #    print c,len(tokenizedTweets),
        for wordIdx in xrange(len(tokenizedTweet)):
            word = tokenizedTweet[wordIdx]  #its a tuple as defined by khanh (word, tag, prob)
            wordtxt = word[0].lower()
            if wordtxt in dictKeys and ((word[1] not in ignoreTags) and (word[2] > threshold) or (word[1] in ignoreTags and word[2] < threshold)):
                tokenizedTweet[wordIdx] = (d1[wordtxt], word[1], word[2]);
    return tokenizedTweets



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

