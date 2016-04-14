from featureExtract.demo import *
from utilities.readTweet import *
import os, json, string
import io

def GroupTweetTokenizer(Groupoptions):      # e.g. GroupTweetTokenizer({'condition':'control'})
    #print 'hello'
    CMUParserLoc = '../ark-tweet-nlp-0.3.2/'
    csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'

    controlFolder = '../data/clpsych2015/schizophrenia/anonymized_control_tweets/'
    schizoFolder ='../data/clpsych2015/schizophrenia/anonymized_schizophrenia_tweets/'

    x = readCSV(csvFileLoc,Groupoptions)

    allControlWithTweets = getTweetsForGroup(x, controlFolder, schizoFolder, fields = ['text'])   #read tweet files and only keep the text part
    allControlText = getFieldFromGroup(allControlWithTweets, 'text')  #convert it to a list of strings
    CreateListofTokens(allControlText,CMUParserLoc)


def CreateListofTokens(alltext,CMUParserLoc):
    options = '--output-format conll '
    Dict = []
    f = open('tweets_control.txt', 'w')
    for t in alltext:
        f.write(t.encode('ascii', 'ignore')+'\n')
    f.close()
    os.system(CMUParserLoc + 'runTagger.sh ' + options + '../schizophreniaThroughTweets/tweets_control.txt > TwokenizerOut_tweets_control.txt')
    os.remove('tweets_control.txt')

    f = open('TwokenizerOut_tweets_control.txt', 'r')
    L = []
    for l in f:
        if l == '\n':
            Dict.append(L)
            L = []
            continue
        values = l.split("\t")
        L.append(values[0])

    f.close()
    os.remove('TwokenizerOut_tweets_control.txt')
    #Dict.append(L)


    with open('data.txt', 'w') as outfile:
        json.dump(Dict, outfile)


GroupTweetTokenizer({'condition':'control'})
