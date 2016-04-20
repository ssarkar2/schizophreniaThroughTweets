from utilities.normalizeTweets import *

tweetList = ['this is a message', 'and a second message :)', 'how u doin?']

[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList)

print tweetList
print cleanedOriginalTweets  #['this is a message', 'and a second message :)', 'how you doing ?']
