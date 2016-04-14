#https://github.com/brendano/ark-tweet-nlp/
#https://code.google.com/archive/p/ark-tweet-nlp/downloads
from utilities.readTweet import *
import os

CMUParserLoc = '../../ark-tweet-nlp-0.3.2/'

def CMURunTaggerSingleTweetFile(tweetFile, num = None, options = ''):  #1st num number of tweets are parsed. If its None, all are parsed
    t = readTweetsFromFile(tweetFile)
    f = open('mytemptext.txt', 'w')
    for tweet in t:  #tweet is a dictionary representing a tweet
        f.write(tweet['text'].encode('ascii','ignore') +'\n')   #note if 'text' does not exist it will throw an error. handle that if it occurs. should not happen though
        #note special unicode characters are ignored. replaced by ?
    f.close()
    os.system(CMUParserLoc + 'runTagger.sh ' + options + ' mytemptext.txt')
    os.remove('mytemptext.txt')



