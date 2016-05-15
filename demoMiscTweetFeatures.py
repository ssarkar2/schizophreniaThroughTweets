import cPickle as pickle
import os, timeit, csv
from utilities.readTweet import *
import numpy as np
from scipy.stats import ttest_ind

def getUserDictForMultFields(tweetGroup, fds):  #fds is fields
    return {user['anonymized_name']:{fd:[tw.get(fd,None) for tw in user['tweets']] for fd in fds} for user in tweetGroup}

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
        allGroupTweets = getUserDictForMultFields(allGroupTweets, fds) #{usr1:{'created_at':[3,0,...], 'retweeted':['false', 'true',...],...}, usr2:{}}
        print 'got tweets', timeit.default_timer() - start
        with open(picklefile, 'w') as f:
            pickle.dump(allGroupTweets, f)
    return allGroupTweets

def dumpToCSV(featuresDict, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for user in featuresDict:
            writer.writerow([user] + featuresDict[user])

def getFeatures(group, key, functions):
    return {user:[f(group[user][key]) for f in functions] for user in group}

def getSubFeatures(group, key, subkey, functions):
    return {user:[f([i[subkey] for i in group[user][key]]) for f in functions] for user in group}


def generateFeatures1(allControlTweets, allSchTweets, key, functions):
    dumpToCSV(getFeatures(allControlTweets, key, functions), 'control_'+key+'.csv')
    dumpToCSV(getFeatures(allSchTweets, key, functions), 'sch_'+key+'.csv')

def generateFeatures2(allControlTweets, allSchTweets, mainkey, subkeys, functions):
    for subkey in subkeys:
        dumpToCSV(getSubFeatures(allControlTweets, mainkey, subkey, functions), 'control_'+mainkey+'_'+subkey+'.csv')
        dumpToCSV(getSubFeatures(allSchTweets, mainkey, subkey, functions), 'sch_'+mainkey+'_'+subkey+'.csv')


allControlTweets = getData({'condition':'control'}, ['favorite_count', 'retweeted', 'user', 'retweet_count'], picklefile = 'dumpdata1_miscfeatures_ctrl.pickle')
allSchTweets = getData({'condition':'schizophrenia'}, ['favorite_count', 'retweeted', 'user', 'retweet_count'], picklefile = 'dumpdata1_miscfeatures_sch.pickle')

generateFeatures1(allControlTweets, allSchTweets, 'favorite_count', [np.mean, np.var, np.max, np.min, lambda lst:sum(np.asarray(lst)==0)/(len(lst)+0.)])  #the lambda function calculates the percentage of 0 values
print 'fav count done'
generateFeatures1(allControlTweets, allSchTweets, 'retweeted', [lambda lst:sum([1 for i in lst if i == 'false'])/(len(lst)+0.)]) #the lambda function calculates the percentage of occurance of 'false'
print 'retweeted done'
generateFeatures1(allControlTweets, allSchTweets, 'retweet_count', [np.mean, np.var, np.max, np.min, lambda lst:sum(np.asarray(lst)==0)/(len(lst)+0.)])
generateFeatures2(allControlTweets, allSchTweets, 'user', ['statuses_count', 'friends_count', 'followers_count', 'favourites_count'], [np.mean, np.var, np.max, np.min, lambda lst:sum(np.asarray(lst)==0)/(len(lst)+0.)])