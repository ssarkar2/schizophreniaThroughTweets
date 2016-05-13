import cPickle as pickle
import csv

def neologismCount(userGroup, wordlist, filename):
    
    counter = {}
    for user in userGroup:
        print user,
        numwords = 0; numnewwords = 0
        for tweet in userGroup[user]:
            for word in tweet.split(' '):
                numwords += 1
                if word.lower() not in wordlist:
                    numnewwords+=1
        counter[user] = numnewwords/(numwords+0.)

    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for user in counter:
            writer.writerow([user, counter[user]])
        
    return counter

picklefile = 'dumpdata1_rhyme.pickle'  #using the rhyme pickle file as its the same data
with open(picklefile) as f:
    allControlTweets, allSchTweets = pickle.load(f)
    
print;
wordlist = set([i.strip() for i in open('utilities/engWords.txt', 'r').read().split('\n')])
print neologismCount(allControlTweets, wordlist, 'control_neologismcount.csv'); print
print neologismCount(allSchTweets, wordlist, 'sch_neologismcount.csv')