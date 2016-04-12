import os, gzip, json

def readTweet(inpFile):  #can read both gz and extracted tweets
    if (inpFile.split('.')[-1] == 'gz'):
        return json.loads(gzip.open(inpFile, 'rb').readline())
    else:
        return json.loads(open(inpFile, 'rb').readline())

a = readTweet('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\7VbnLI9dA.txt')
b = readTweet('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\7VbnLI9dA.tweets.gz')
print a
print
print
print b