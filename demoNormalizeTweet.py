from utilities.normalizeTweets import *

tweetList = ['this is a message', 'and a second message :)', 'how u doin?', 'wrong spellng', 'See them @ http://t.co/zfqCluAHSx http://t/aMlnqIpR2XmJkF5ybVZfi2xcgPa2026', '! @ # $ % ^ & * ( ) _ +', 'at of it']

[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList, ops = [0,1])

print tweetList
#print tokenizedTweets
print cleanedOriginalTweets  #['this is a message', 'and a second message :)', 'how you doing ?', 'wrong spelling', 'see them a http://t.co/zfqCluAHSx http://t/aMlnqIpR2XmJkF5ybVZfi2xcgPa2026']


[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList, ops = [0])
print tweetList
#print tokenizedTweets
print cleanedOriginalTweets  #['this is a message', 'and a second message :)', 'how you doing ?', 'wrong spellng', 'See them @ http://t.co/zfqCluAHSx http://t/aMlnqIpR2XmJkF5ybVZfi2xcgPa2026', '! @ # $ % ^ & * ( ) _ +', 'at of it']
