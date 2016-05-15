import cPickle as pickle
import os, timeit, csv
from utilities.normalizeTweets import *
from utilities.readTweet import *
import numpy as np

def getData(): #returns 2 lists of strings for the 2 groups
    control_folder_path = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
    sch_folder_path = '../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'
    csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
    picklefile = 'dumpdata1_rhyme.pickle'  #using the rhyme pickle file as its the same data
    if os.path.isfile(picklefile):
        with open(picklefile) as f:
            allControlTweets, allSchTweets = pickle.load(f)
    else:
        #read lines of csv
        allControl = readCSV(csvFileLoc, {'condition':'control'})
        allSch = readCSV(csvFileLoc, {'condition':'schizophrenia'})

        #get tweets by read files.
        start = timeit.default_timer()
        allControlTweets = getTweetsForGroup(allControl, control_folder_path, sch_folder_path, fields = ['text'])  #read the files and get the tweet (only the text as specified in 'field')
        allSchTweets = getTweetsForGroup(allSch, control_folder_path, sch_folder_path, fields = ['text'])
        allControlTweets = getFieldDictFromGroupPerUser(allControlTweets, field = 'text')
        allSchTweets = getFieldDictFromGroupPerUser(allSchTweets, field = 'text')
        print 'got tweets', timeit.default_timer() - start

        with open(picklefile, 'w') as f:
            pickle.dump([allControlTweets, allSchTweets], f)
    return [allControlTweets, allSchTweets]

def cleanup(tt): #do spell check, separate out hashtags and add that to spellchecked text
    t = {k:normTweet1(tt[k], ops = [0], retain = 2, separateTokens = ['E'])[0] for k in tt}
    return {k:[(' ').join([word[0] for word in singletweet]) for singletweet in t[k][-1]] for k in t}

def getSentimentDict():
    d = {'positive':1, 'negative':-1, 'neutral':0}
    with open('connotation_lexicon_a.0.1.csv', 'r') as fn:
        t = [line.split(',') for line in fn.read().split('\n')]
        return {line[0].split('_')[0]:d[line[1]] for line in t[0:-1]}

def getSentimentDict1():
    with open('utilities/AFINN-111.txt','r') as f:
        t = [line.split('\t') for line in f.read().split('\n')]
    return {line[0]:int(line[1]) for line in t}


def getSentiFeatures(scoreList, counts): #scorelist is a list of lists containing only 1,-1,0 or 'x'
    #counts of sentiments
    #counts = {1:0, -1:0, 0:0, 'x':0} #[pos, neg, neu, unk]
    countsOrig = {k:counts[k] for k in counts}
    for singleTweetScores in scoreList:
        counts = {k:countsOrig[k] for k in countsOrig}
        for singleTweetScore in singleTweetScores:
            #print counts, singleTweetScore, singleTweetScore in counts.keys()
            #print counts.keys()
            counts[singleTweetScore]+=1
    ft =  [counts[k]/(sum(counts.values())+0.) for k in counts]  #return normalized counts

    #mean/var of tweet sentiment score
    tweetScores = [sum([singleTweetScore for singleTweetScore in singleTweetScores if singleTweetScore != 'x']) for singleTweetScores in scoreList]
    ft += [np.mean(tweetScores), np.var(tweetScores), max(tweetScores)]
    return ft

def calculateSentimentFeatures(userTweetDict, sentDict, csvName, counts):
    t = {user:getSentiFeatures([[sentDict.get(word,'x') for word in tweet.split(' ')] for tweet in userTweetDict[user]], counts) for user in userTweetDict}  #'x' is for words not in the senti dictionary
    with open(csvName, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for user in t:
            writer.writerow([user] + t[user])


print 'start'
[allControlTweets, allSchTweets] = getData()

picklefile = 'dumpdata2_rhyme.pickle'  #using the rhyme pickle file as its the same data
if os.path.isfile(picklefile):
    with open(picklefile) as f:
        allControlTweetsCleaned, allSchTweetsCleaned = pickle.load(f)
else:
    print 'clean allControlTweets'
    allControlTweetsCleaned = cleanup(allControlTweets)
    print 'clean allControlTweets'
    allSchTweetsCleaned = cleanup(allSchTweets)
    with open(picklefile, 'w') as f:
        pickle.dump([allControlTweetsCleaned, allSchTweetsCleaned], f)


sentDict = getSentimentDict()
calculateSentimentFeatures(allControlTweetsCleaned, sentDict, 'control_simpleconnotation_features.csv', {1:0, -1:0, 0:0, 'x':0})
calculateSentimentFeatures(allSchTweetsCleaned, sentDict, 'sch_simpleconnotation_features.csv', {1:0, -1:0, 0:0, 'x':0})


sentDict = getSentimentDict1() #AFINN
calculateSentimentFeatures(allControlTweetsCleaned, sentDict, 'control_simplesentimentAFINN_features.csv', {1:0, -1:0, 0:0, 2:0, -2:0, 3:0, -3:0, 4:0, -4:0, 5:0, -5:0, 'x':0})
calculateSentimentFeatures(allSchTweetsCleaned, sentDict, 'sch_simplesentimentAFINN_features.csv', {1:0, -1:0, 0:0, 2:0, -2:0, 3:0, -3:0, 4:0, -4:0, 5:0, -5:0, 'x':0})