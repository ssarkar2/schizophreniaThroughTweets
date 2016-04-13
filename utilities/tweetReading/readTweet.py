import os, gzip, json

def getIDFromFilename(filename):  #get unique id from file name
    return filename.split('\\')[-1].split('.')[0]

def readTweet(inpFile):  #can read both gz and extracted tweets
    openfunc = (open, gzip.open)[inpFile.split('.')[-1] == 'gz']  #choose a open function based on if its compressed or not
    return (getIDFromFilename(inpFile), [json.loads(i) for i in openfunc(inpFile, 'rb').read().split('\n') if len(i) > 0])  #return a tuple (id, list of dictionaries). each dictionary is a tweet


def getAllTweets(inpFolder):
    return [readTweet(inpFolder+filename) for filename in os.listdir(inpFolder)]



#read single tweet
a = readTweet('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\bebChK7PskxB.txt')
print 'done'
b = readTweet('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\bebChK7PskxB.tweets.gz')
##print a
##print
##print
##print b

alltweets = getAllTweets('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\')
print len(alltweets)
print alltweets[0][0]