import cPickle as pickle
import csv
import numpy as np


def schCounter(userGroup, filename):      
    flagWords = ['schizophre', 'insane', 'paranoia', 'hallucin', 'confus', 'medic', 'symptom']  
    schCount = {user:[0]*len(flagWords) for user in userGroup}
    for user in userGroup:
        #print user
        for tweet in userGroup[user]:
            for word in tweet.split(' '):
                for flagWordIdx in range(len(flagWords)):
                    if flagWords[flagWordIdx] in word.lower():
                        #print tweet,
                        schCount[user][flagWordIdx] += 1
        schCount[user] = [item/(len(userGroup[user])+0.) for item in schCount[user]]
        
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for user in schCount:
            writer.writerow([user] + schCount[user])
    print [np.mean([i[xx] for i in schCount.values()]) for xx in range(len(flagWords))]
    return schCount
                    

picklefile = 'dumpdata1_rhyme.pickle'  #using the rhyme pickle file as its the same data
with open(picklefile) as f:
    allControlTweets, allSchTweets = pickle.load(f)
  


                
                

print;
print schCounter(allControlTweets, 'control_schcount.csv'); print
print schCounter(allSchTweets, 'sch_schcount.csv')