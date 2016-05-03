import cPickle as pickle
import os, timeit
from utilities.readTweet import *
from utilities.normalizeTweets import normTweet1
from utilities.rhymingWords import *
import csv
import numpy as np
from scipy.stats import ttest_ind

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



picklefile = 'dumpdata3_rhyme.pickle'
with open(picklefile) as f:
    rhymingScoresControl, rhymingScoresSch = pickle.load(f)

mnCtrl = []; vrCtrl = []; zerCtrl = []; nonzerCtrl = []
mnSch = []; vrSch = []; zerSch = []; nonzerSch = []
with open('RhymeFeaturesCtrl.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for user in rhymingScoresControl:
        scores = rhymingScoresControl[user]
        mn = np.nanmean([np.mean(i) for i in scores])  #nanmean ignores nans. nan may occur if mean of [] (empty) array is taken
        vr = np.nanmean([np.var(i) for i in scores])
        zer = 0.; nonzer = 0.
        for i in scores:
            for j in i:
                if j==0:
                    zer+=1
                else:
                    nonzer+=1
        mnCtrl += [mn]; vrCtrl += [vr]; zerCtrl += [zer/(zer+nonzer)]; nonzerCtrl += [nonzer/(zer+nonzer)];
        writer.writerow([user, mn, vr, zer/(zer+nonzer), nonzer/(zer+nonzer)])
with open('RhymeFeaturesSch.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for user in rhymingScoresSch:
        scores = rhymingScoresSch[user]
        mn = np.nanmean([np.mean(i) for i in scores])
        vr = np.nanmean([np.var(i) for i in scores])
        zer = 0.; nonzer = 0.
        for i in scores:
            for j in i:
                if j==0:
                    zer+=1
                else:
                    nonzer+=1
        mnSch += [mn]; vrSch += [vr]; zerSch += [zer/(zer+nonzer)]; nonzerSch += [nonzer/(zer+nonzer)];
        writer.writerow([user, mn, vr, zer/(zer+nonzer), nonzer/(zer+nonzer)])

#concatControl = []
#for i in rhymingScoresControl:
#    concatControl += rhymingScoresControl[i]

#concatSch = []
#for i in rhymingScoresSch:
#    concatSch += rhymingScoresSch[i]


print 't test mean', ttest_ind(mnCtrl, mnSch)
print 't test var', ttest_ind(vrCtrl, vrSch)
print 't test zero', ttest_ind(zerCtrl, zerSch)
print 't test nonzero', ttest_ind(nonzerCtrl, nonzerSch)
"""
t test mean Ttest_indResult(statistic=-4.7560304698663938, pvalue=3.2066866234498495e-06)
t test var Ttest_indResult(statistic=-5.3343641528416716, pvalue=2.0198713087689003e-07)
t test zero Ttest_indResult(statistic=4.6420513477542551, pvalue=5.3721995651696209e-06)
t test nonzero Ttest_indResult(statistic=-4.6420513477542356, pvalue=5.3721995651701003e-06)
"""

"""
t test mean Ttest_indResult(statistic=-3.900886273598184, pvalue=0.00012084652671746473)
t test var Ttest_indResult(statistic=-4.5176265439826215, pvalue=9.3314325366263576e-06)
t test zero Ttest_indResult(statistic=4.1322320325847013, pvalue=4.7872826011918165e-05)
t test nonzero Ttest_indResult(statistic=-4.1322320325847146, pvalue=4.7872826011915651e-05)
"""