from utilities.normalizeTweets import *
from utilities.normalizeTweets import *



tweetList = ['this is a message', 'and a second message :)', 'how u doin?', 'wrong spellng', 'See them @ http://t.co/zfqCluAHSx http://t/aMlnqIpR2XmJkF5ybVZfi2xcgPa2026', '! @ # $ % ^ & * ( ) _ +', 'at of it', 'that was funny, lol lmao brb ttyl IBM! (>_<)', '#hello hello #byeWrld #HelloWorldIBMWow :P']

[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList, ops = [0,1])  #detailed description of normTweet1 is available in normalizeTweets

print tweetList
#print tokenizedTweets
print cleanedOriginalTweets
print tokenizedTweets[0]


[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList, ops = [0], retain = 1, separateTokens = [])
print tweetList
#print tokenizedTweets
print cleanedOriginalTweets
print tokenizedTweets[0]
print tokenizedTweets
print 'ending here'


tweetList = ['#helloBye there', 'an :) #spelingMistake', 'Wrld' ]
[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList, ops = [0,1], retain = 0)
print tokenizedTweets
print cleanedOriginalTweets



tweetList = ['#helloBye there', 'an :) #spelingMistake', 'Wrld wrld' ]
[tokenizedTweets, cleanedOriginalTweets] = normTweet1(tweetList, ops = [0,1], retain = 1, separateTokens = ['#', 'E'])  #separateTokens = [] if you do not want to separate out # and E
print tokenizedTweets  #[[[('hello bye', '#', 0.765)], [('spe ling mistake', '#', 0.8214)], []], [[], [(':)', 'E', 0.9852)], []], [[('#helloBye', '#', 0.765), ('there', 'R', 0.5307)], [('an', 'D', 0.7642), (':)', 'E', 0.9852), ('#spelingMistake', '#', 0.8214)], [('world', '^', 0.3878), ('world', '^', 0.4131)]]]
print cleanedOriginalTweets  #['#helloBye there', 'an :) #spelingMistake', 'world world']
