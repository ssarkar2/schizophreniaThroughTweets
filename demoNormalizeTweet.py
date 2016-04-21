from utilities.normalizeTweets import *

tweetList = ['this is a message', 'and a second message :)', 'how u doin?', 'wrong spellng']

[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList)

print tweetList
#print tokenizedTweets
print cleanedOriginalTweets  #['this is a message', 'and a second message :)', 'how you doing ?']
