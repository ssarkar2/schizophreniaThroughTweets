import os, gzip, json

def getIDFromFilename(filename):  #get unique id from file name
    return filename.split('\\')[-1].split('.')[0]

def readTweet(inpFile):  #can read both gz and extracted tweets
    openfunc = (open, gzip.open)[inpFile.split('.')[-1] == 'gz']  #choose a open function based on if its compressed or not
    return (getIDFromFilename(inpFile), [json.loads(i) for i in openfunc(inpFile, 'rb').read().split('\n') if len(i) > 0])  #return a tuple (id, list of dictionaries). each dictionary is a tweet


def getAllTweets(inpFolder):  #return all tweets from all users in a directory. takes time to run
    return [readTweet(inpFolder+filename) for filename in os.listdir(inpFolder)]

def readCSV(filename, categoryFilter = None, numFilter = None):
    info = []
    fcsv = open(filename, 'r')
    for row in fcsv.read().split('\n')[1:]:  #dropping the first row as it contains col names
        elements = row.split(',')
        if len(elements) == 6:
            entry = {'anonymized_name':elements[0], 'condition':elements[1], 'age':float(elements[2]), 'gender':elements[3], 'num_tweets':int(elements[4]), 'fold':int(elements[5])}
            if checkCategoryFilter(entry, categoryFilter) and checkNumberFilter(entry, numFilter):
                info.append(entry)
    fcsv.close()
    return info

def checkCategoryFilter(entry, categoryFilter): # categoryFilter is a dictionary like {'condition':'control', 'gender':'M'}
    if categoryFilter == None:  #no filter present, so append all entries to return list
        return True
    else:
        for i in categoryFilter:
            if not(entry[i] in categoryFilter[i]):
                return False #even if one fails, return false
        return True  #all checks passed. return True

def checkNumberFilter(entry, numFilter):
    if numFilter == None:  #no filter present, so append all entries to return list
        return True
    else:
        for i in numFilter:
            retVal = False
            for numRange in numFilter[i]:
                if entry[i]>=numRange[0] and entry[i]<=numRange[1]:
                    retVal = True
            if retVal == False:
                return False
        return True





#read single tweet
#a = readTweet('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\bebChK7PskxB.txt')
#print 'done'
#b = readTweet('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\bebChK7PskxB.tweets.gz')
##print a
##print
##print
##print b

#read all tweets in a folder
#alltweets = getAllTweets('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\')
#print len(alltweets)
#print alltweets[0][0]


print readCSV('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_user_manifest.csv')
print; print
x = readCSV('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_user_manifest.csv', {'condition':'control', 'gender':'M', 'fold':[1,2]}, {'age':[(20,22), (23,25)], 'num_tweets':[(1,1000),(2000,5000)]})
print x