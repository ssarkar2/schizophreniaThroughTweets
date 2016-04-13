import os, gzip, json

def getIDFromFilename(filename):  #get unique id from file name
    return filename.split('\\')[-1].split('.')[0]

def readTweetsFromFile(inpFile, tweetFilterFunc = lambda x: True, fields = None):  #can read both gz and extracted tweets. tweetFilterFunc should be a function that takes in a tweet (dict) and return true/false
    openfunc = (open, gzip.open)[inpFile.split('.')[-1] == 'gz']  #choose a open function based on if its compressed or not
    returnTweetList = []
    for i in openfunc(inpFile, 'rb').read().split('\n'):
        if len(i) > 0:
            t = json.loads(i)
            if tweetFilterFunc(t):
                returnTweetList += ([t], [{k:t[k] for k in fields}])[fields != None]  #if fields == None retain all fields, else retain only those passed as a list in fields parameter
    return returnTweetList

def getAllTweets(inpFolder, tweetFilterFunc = lambda x: True, fields = None):  #return all tweets from all users in a directory. takes time to run.
    return [readTweetsFromFile(inpFolder+filename, tweetFilterFunc, fields) for filename in os.listdir(inpFolder)]

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


def getNamesFromGroup(g):  #get all the anonymized names from a group
    return [entry['anonymized_name'] for entry in g]

def setOpsGroups(groupList, setFunc): #performs: A setfunc B setfunc C...
    nameSet = set(getNamesFromGroup(groupList[0]))
    for grp in groupList[1:]:
        nameSet = setFunc(nameSet, set(getNamesFromGroup(grp)))
    nameList = list(nameSet)
    joinedGroup = []
    for grp in groupList:
        for entry in grp:
            if entry['anonymized_name'] in nameList :
                joinedGroup += [entry]
                nameList.remove(entry['anonymized_name'])
    return joinedGroup


def getTweetsForGroup(grp, controlFolder, schizoFolder, tweetFilterFunc = lambda x: True, fields = None):  #the folders should contain the zipped files, not uncompressed ones
    for entry in grp:
        entry['tweets'] = readTweetsFromFile((schizoFolder, controlFolder)[entry['condition'] == 'control'] + entry['anonymized_name'] + '.tweets.gz', tweetFilterFunc, fields)
    return grp


def demo():
    #read single tweet
    #a = readTweetsFromFile('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\bebChK7PskxB.txt')
    #print 'done'
    #b = readTweetsFromFile('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\bebChK7PskxB.tweets.gz')
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
    y = readCSV('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_user_manifest.csv', {'condition':'control', 'gender':'F', 'fold':[1,2]}, {'age':[(20,22), (23,25)], 'num_tweets':[(1,3000)]})
    z = setOpsGroups([x,y], set.union)
    print len(x), len(y), len(z)
    a = readCSV('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_user_manifest.csv', {'condition':'control', 'gender':'F', 'fold':[1,2]}, {'age':[(20,22), (23,25)], 'num_tweets':[(1,6000)]})
    b = setOpsGroups([y,a], set.union)
    print len(a), len(y), len(b)

    c = setOpsGroups([a,y], set.intersection)
    print a; print; print y; print ; print c

    c = setOpsGroups([a,y], set.union)
    print a; print; print y; print ; print c

    controlFolder = 'C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\'
    schizoFolder = 'C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_schizophrenia_tweets\\'
    d = getTweetsForGroup(y, controlFolder, schizoFolder, tweetFilterFunc = lambda t: 'Sun' in t['created_at'], fields = ['text', 'lang'])
    print d
    print len(d)



    b = readTweetsFromFile('C:\Sayantan\\acads\cmsc773\proj\data\data\clpsych2015\schizophrenia\\anonymized_control_tweets\\bebChK7PskxB.tweets.gz', tweetFilterFunc = lambda t: 'Sun' in t['created_at'], fields = ['text', 'lang'])  #get only 2 fields of tweets made on a sunday
    print b[0]; print; print b[1]; print ; print len(b)
    print b[0:6]
