#find all types of emoticons in the dataset
#perhaps manually assign emotions to them
from utilities.readTweet import *
from utilities.normalizeTweets import tokenizeCMUPython
import os, time
import cPickle as pickle

def writeToFile(fname, data):
    data = list(set(data))
    f = open(fname, 'w')
    for i in data:
        f.write(i + '\n')
    f.close()

csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
controlFolder = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
schFolder = '../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'

fname = 'findEmoticon_all.pickle'
if os.path.isfile(fname):
    print 'Reading from pickled file'
    start_time = time.time()
    with open(fname, 'r') as f:
        tokenizedTweets = pickle.load(f)
    print time.time() - start_time  #76s ~imin
else:
    allData = readCSV(csvFileLoc);
    allTweetText = getTweetsForGroup(allData, controlFolder, schFolder, fields = ['text'])
    #textList = getFieldFromGroupPerUser(allTweetText, field = 'text')
    #textList = [['rere', 'ereteer'], ['rtrtrtrtrt', 'gdfgdf']]. The sublists denote users

    textList = getFieldFromGroup(allTweetText, field = 'text')
    #textList = ['ddfd', 'fdgdg', ...]
    start_time = time.time()
    tokenizedTweets = tokenizeCMUPython(textList)
    print time.time() - start_time  #912s ~15mins
    with open(fname, 'w') as fp:
        pickle.dump(tokenizedTweets, fp)

threshold = 0.7
allEmoticons = []; allHashtags = [];
start_time = time.time()
for tokenizedTweet in tokenizedTweets:  #tokenizedTweet is a list of 3-tuples
    allEmoticons += [word[0] for word in tokenizedTweet if word[1] == 'E' and word[2] > threshold]
    allHashtags += [word[0] for word in tokenizedTweet if word[1] == '#' and word[2] > threshold]
print time.time() - start_time

writeToFile('emoticonList.txt', allEmoticons)
writeToFile('hashtagList.txt', allHashtags)








