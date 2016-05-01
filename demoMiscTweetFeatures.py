import cPickle as pickle
import os, timeit, csv
from utilities.readTweet import *
import numpy as np
from scipy.stats import ttest_ind

def getUserDictForMultFields(tweetGroup, fds):
    return {user['anonymized_name']:{fd:[tw.get(fd,None) for tw in user['tweets']] for fd in fds} for user in tweetGroup}


"""
def getData(fds): #returns 2 lists of strings for the 2 groups
    control_folder_path = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
    sch_folder_path = '../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'
    csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
    picklefile = 'dumpdata1_miscfeatires.pickle'
    if os.path.isfile(picklefile):
        with open(picklefile) as f:
            allControlTweets, allSchTweets = pickle.load(f)
    else:
        #read lines of csv
        allControl = readCSV(csvFileLoc, {'condition':'control'})
        allSch = readCSV(csvFileLoc, {'condition':'schizophrenia'})

        #get tweets by read files.
        start = timeit.default_timer()
        allControlTweets = getTweetsForGroup(allControl, control_folder_path, sch_folder_path, fields = fds)  #read the files and get the tweet (only the text as specified in 'field')
        allSchTweets = getTweetsForGroup(allSch, control_folder_path, sch_folder_path, fields = fds)

        allControlTweets = getUserDictForMultFields(allControlTweets, fds) #{usr1:{'created_at':3, 'retweeted':'false',...}, usr2:{}}
        allSchTweets = getUserDictForMultFields(allSchTweets, fds)

        #allControlTweets = getFieldDictFromGroupPerUser(allControlTweets, field = fds)
        #allSchTweets = getFieldDictFromGroupPerUser(allSchTweets, field = fds)
        print 'got tweets', timeit.default_timer() - start

        with open(picklefile, 'w') as f:
            pickle.dump([allControlTweets, allSchTweets], f)
    return [allControlTweets, allSchTweets]

[allControlTweets, allSchTweets] = getData(['favorite_count', 'retweeted', 'user', 'retweet_count'])
"""

def getData(filter, fds, picklefile):
    control_folder_path = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
    sch_folder_path = '../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'
    csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
    if os.path.isfile(picklefile):
        with open(picklefile) as f:
            allGroupTweets = pickle.load(f)
    else:
        allGroup = readCSV(csvFileLoc, filter)
        #get tweets by read files.
        start = timeit.default_timer()
        allGroupTweets = getTweetsForGroup(allGroup, control_folder_path, sch_folder_path, fields = fds)
        allGroupTweets = getUserDictForMultFields(allGroupTweets, fds) #{usr1:{'created_at':3, 'retweeted':'false',...}, usr2:{}}
        print 'got tweets', timeit.default_timer() - start
        with open(picklefile, 'w') as f:
            pickle.dump(allGroupTweets, f)
    return allGroupTweets

allControlTweets = getData({'condition':'control'}, ['favorite_count', 'retweeted', 'user', 'retweet_count'], picklefile = 'dumpdata1_miscfeatures_ctrl.pickle')
allSchTweets = getData({'condition':'schizophrenia'}, ['favorite_count', 'retweeted', 'user', 'retweet_count'], picklefile = 'dumpdata1_miscfeatures_sch.pickle')

