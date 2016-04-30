import cPickle as pickle
import os, timeit
from utilities.readTweet import *
from utilities.normalizeTweets import normTweet1
from utilities.rhymingWords import *

def getData(): #returns 2 lists of strings for the 2 groups
    control_folder_path = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
    sch_folder_path = '../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'
    csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
    picklefile = 'dumpdata1_rhyme.pickle'
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
    #t = {k:normTweet1(tt[k], ops = [0,1], retain = 2, separateTokens = ['E'])[0] for k in tt} #key:[[[],[],[],[]], [[],[],[],[]], [,[(),(),()],[(),()],[()],[()]]]
    #for k in t:
    #    tmp = t[k]
    #    t[k] = [(' ').join([tpl[0] for tpl in tmp[0][i] + tmp[2][i]]) for i in range(0,len(tmp[0]))] # len(tmp[0]) is num of tweets fro this user. tmp[0] is the hashtags, tmp[2] is the text
    #return t


def getRhymingScores(cleanedTweets, entries):  #cleanedTweetsis a dict. username is key, and val is a list of strings (user's cleaned tweets)
    return {user:getRhymingScoreForText(cleanedTweets[user], entries) for user in cleanedTweets}

print 'start'
[allControlTweets, allSchTweets] = getData()

picklefile = 'dumpdata2_rhyme.pickle'
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
        
        

print 'calc rhyming scores'
picklefile = 'dumpdata3_rhyme.pickle'
if os.path.isfile(picklefile):
    with open(picklefile) as f:
        rhymingScoresControl, rhymingScoresSch = pickle.load(f)
else:   
    entries = getWordSyllableDict()
    rhymingScoresControl = getRhymingScores(allControlTweetsCleaned, entries)
    rhymingScoresSch = getRhymingScores(allSchTweetsCleaned, entries)
    with open(picklefile, 'w') as f:
        pickle.dump([rhymingScoresControl, rhymingScoresSch], f)