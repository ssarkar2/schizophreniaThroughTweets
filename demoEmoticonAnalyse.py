import cPickle as pickle
import os, timeit, csv
from utilities.normalizeTweets import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from utilities.readTweet import *
from scipy.stats import ttest_ind
import scipy.io as sio

def getData(): #returns 2 lists of strings for the 2 groups
    control_folder_path = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
    sch_folder_path = '../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'
    csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
    picklefile = 'dumpdata1_emo.pickle'
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

def getEmoticonAnnotation(emoticonAnnotatedFile):
    t = [i.split(' ') for i in  open(emoticonAnnotatedFile).read().split('\n')]
    return {i[0]:float(i[3]) for i in t if len(i) == 4}

def getEmoticonFeature(emoList, emoticonScoreDict):  #emoList = [[':)', ':P'], [], [':(']]. empty lists denote those tweets did not have emoticons in their text
    emoScore = {user:[emoticonScoreDict.get(emo[0],0) for emo in emoList[user]] for user in emoList}
    retval = {}
    for user in emoScore:
        t = emoScore[user]
        retval[user] = ((np.mean(t), np.var(t), len(t)), (0.,0.,0))[len(t)==0]
    return retval
    #return {user:((np.mean(emoScore[user]), np.var(emoScore[user]), len(emoScore[user])), (0.,0.,0))[len(emoScore[user])==0] for user in emoScore}  #list of 3-tuples. each tuple is the emoticon feature for that tweet (mean, variance, number of emoticons)



print 'start'
[allControlTweets, allSchTweets] = getData()

picklefile = 'dumpdata2_emo.pickle'
if os.path.isfile(picklefile):
    with open(picklefile) as f:
        normControl, normSch = pickle.load(f)
else:
    start = timeit.default_timer()
    #normControl = {user:normTweet1(allControlTweets[user], ops = [], retain = 1, separateTokens = ['E'])[0][0] for user in allControlTweets}  #being lazy here. the emoticons AND the text is also returned by normTweet1. We dont need the text for this exercise
    normControl = {}
    C = 0
    for user in allControlTweets:
        print 'CTRL', user, C; C+=1
        normControl[user] = normTweet1(allControlTweets[user], ops = [], retain = 1, separateTokens = ['E'])[0][0]
    print 'got normControl', timeit.default_timer() - start  #387s
    start = timeit.default_timer()
    #normSch = {user:normTweet1(allSchTweets[user], ops = [], retain = 1, separateTokens = ['E'])[0][0] for user in allSchTweets}
    normSch = {}
    C=0
    for user in allSchTweets:
        print 'SCH', user,C; C+=1
        normSch[user] = normTweet1(allSchTweets[user], ops = [], retain = 1, separateTokens = ['E'])[0][0]
    print 'got normSch', timeit.default_timer() - start  #384s
    with open(picklefile, 'w') as f:
        pickle.dump([normControl, normSch], f)

'''
controlEmo = {}
for user in normControl:
    print user
    for emo in normControl[user]:
        print emo
    controlEmo[user] = [emo[0] for emo in normControl[user] i]
    '''

controlEmo = {user:[emo[0] for emo in normControl[user] if emo != []] for user in normControl}  #key is username, value is of the form [[(':)', 'E', 0.9), (':P', 'E', 0.99)],  []]
schEmo =     {user:[emo[0] for emo in normSch[user] if emo != []] for user in normSch}


emoticonScoreDict = getEmoticonAnnotation('utilities/emoticonList_annotated.txt')
controlFeat = getEmoticonFeature(controlEmo, emoticonScoreDict)
schFeat = getEmoticonFeature(schEmo, emoticonScoreDict)


#3d plots
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
xc = {user:controlFeat[user][0] for user in controlFeat}; yc = {user:controlFeat[user][1] for user in controlFeat}; zc = {user:controlFeat[user][2] for user in controlFeat}
xs = {user:schFeat[user][0] for user in schFeat}; ys = {user:schFeat[user][1] for user in schFeat}; zs = {user:schFeat[user][2] for user in schFeat}

#ax.scatter(xs, ys, zs, c='r', marker='o')
#ax.scatter(xc, yc, zc, c='b', marker='^')
#ax.set_xlabel('Mean')
#ax.set_ylabel('Variance')
#ax.set_zlabel('Number')

#2d plots
#plt.plot(xs, ys, 'r^', xc, yc, 'bs'); plt.show()
#plt.plot(xs, zs, 'r^', xc, zc, 'bs'); plt.show()
#plt.plot(zs, ys, 'r^', zc, yc, 'bs'); plt.show()

#sio.savemat('emoticonAnalyse.mat', {'xc':xc, 'yc':yc, 'zc':zc, 'xs':xs, 'ys':ys, 'zs':zs})

with open('emoticonFeaturesCtrl.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for user in controlFeat:
        writer.writerow([user, xc[user], yc[user], zc[user]])


with open('emoticonFeaturesSch.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for user in schFeat:
        writer.writerow([user, xs[user], ys[user], zs[user]])



print 'mean of ft 1', np.mean(xc.values()), np.mean(xs.values())
print 'mean of ft 2', np.mean(yc.values()), np.mean(ys.values())
print 'mean of ft 3', np.mean(zc.values()), np.mean(zc.values())
print '# of tweets in each group', len(controlFeat), len(schFeat)

print 't test feat 1', ttest_ind(xc.values(), xs.values())
print 't test feat 2', ttest_ind(yc.values(), ys.values())
print 't test feat 3', ttest_ind(zc.values(), zs.values())

'''
mean of ft 1 0.044251820544 0.0407166580237
mean of ft 2 0.00308961606865 0.00207638773401
mean of ft 3 0.120600806558 0.120600806558
# of tweets in each group 530154 529257
t test feat 1 Ttest_indResult(statistic=6.4992050181153491, pvalue=8.0781157244368766e-11)
t test feat 2 Ttest_indResult(statistic=14.252762789068353, pvalue=4.351486585757677e-46)
t test feat 3 Ttest_indResult(statistic=23.042523842720197, pvalue=1.8687147480576763e-117)