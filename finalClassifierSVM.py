import csv
from utilities.readTweet import readCSV
from sklearn import svm
import numpy as np


def csvReader(csvLoc, colMask):  #input is csv file loc and the masking array. out is a dict. key is username, value is a list of features that are not masked out.
    return {row[0]: [float(row[num+1]) for num in range(len(row[1:])) if colMask[num] == 1] for row in csv.reader(open(csvLoc, 'rb'), delimiter=',')}
       
def getAllFeatures(csvList, useFeatures):
    featuresDicts = [csvReader('resultsDump/allCSVs/' + csvFile, useFeatures[csvFile]) for csvFile in csvList]
    return {k:sum([dic[k] for dic in featuresDicts], []) for k in featuresDicts[0].keys()}  #first make a list of lists of features for each user, then flatten it using sum(L,[])
    
def normFeatParams(X):
    a = np.asarray(X)
    return [np.mean(a,0), np.std(a,0)]
    
def normFeat(X, mn, s):
    return [[(userFt[ftid]-mn[ftid])/s[ftid] for ftid in range(len(userFt))] for userFt in X]
    
def getAccuracy(gt, pred):
    return sum([1 for i in range(len(gt)) if gt[i]==pred[i]])/(len(gt)+0.)

#this file is written assuming that there are 2 csvs for each feature (control and sch)
csvList = [['control_favorite_count.csv', 'control_simpleconnotation_features.csv', 'control_user_favourites_count.csv', 'control_user_followers_count.csv', 'control_user_friends_count.csv', 'control_user_statuses_count.csv', 'emoticonFeaturesCtrl.csv', 'RhymeFeaturesCtrl.csv', 'RhymeFeaturesCtrl1.csv'], 
           ['sch_favorite_count.csv', 'sch_simpleconnotation_features.csv', 'sch_user_favourites_count.csv', 'sch_user_followers_count.csv', 'sch_user_friends_count.csv', 'sch_user_statuses_count.csv', 'emoticonFeaturesSch.csv', 'RhymeFeaturesSch.csv', 'RhymeFeaturesSch1.csv']]
       
useFeatures = {'control_favorite_count.csv':[0,0,1,0,1], 'sch_favorite_count.csv':[0,0,1,0,1],
                'control_simpleconnotation_features.csv':[1,1,1,1,1,1,0], 'sch_simpleconnotation_features.csv':[1,1,1,1,1,1,0],
                'control_user_favourites_count.csv':[1,0,1,1,0], 'sch_user_favourites_count.csv':[1,0,1,1,0],
                'control_user_followers_count.csv':[0,0,0,0,0], 'sch_user_followers_count.csv':[0,0,0,0,0],
                'control_user_friends_count.csv':[0,0,0,0,0], 'sch_user_friends_count.csv':[0,0,0,0,0],
                'control_user_statuses_count.csv':[1,0,1,1,0], 'sch_user_statuses_count.csv':[1,0,1,1,0],
                'emoticonFeaturesCtrl.csv':[1,0,1,1,0], 'emoticonFeaturesSch.csv':[1,0,1,1,0],
                'RhymeFeaturesCtrl.csv':[1,1,1,1], 'RhymeFeaturesSch.csv':[1,1,1,1],
                'RhymeFeaturesCtrl1.csv':[1,1,1,1], 'RhymeFeaturesSch1.csv':[1,1,1,1]
               }
               
               
#print csvReader('resultsDump/allCSVs/' + csvList[0][0], useFeatures[csvList[0][0]])

control = getAllFeatures(csvList[0], useFeatures)  #{'u1':[1,3,2,4,3...], 'u2':[...], ...}
sch = getAllFeatures(csvList[1], useFeatures)
#print len(control) #137
#print len(control['bebChK7PskxB']) #24
#print control['bebChK7PskxB']  #24 features in all

csvFileLoc = '../data/clpsych2015/schizophrenia/anonymized_user_manifest.csv'
#allControlPerFold = {foldid:[user['anonymized_name'] for user in readCSV(csvFileLoc, {'condition':'control','fold':[foldid]})] for foldid in range(0,10)}  #its a dictionary with 10 keys 0 to 9 (the folds) and the values are lists of user names in that fold: {0:['u1', 'u2'], 1:[...], ...}
#allSchPerFold = {foldid:[user['anonymized_name'] for user in readCSV(csvFileLoc, {'condition':'schizophrenia','fold':[foldid]})] for foldid in range(0,10)} 
#print allControlPerFold
#print allSchPerFold

controlUserFoldDict = {user['anonymized_name']:user['fold'] for user in readCSV(csvFileLoc, {'condition':'control'})}  #dict of length 137, with users as keys and their folds as values
schUserFoldDict = {user['anonymized_name']:user['fold'] for user in readCSV(csvFileLoc, {'condition':'schizophrenia'})}
print controlUserFoldDict

#SVM
accuracy = []
for foldid in range(10):
    controlTest = [control[user] for user in controlUserFoldDict if controlUserFoldDict[user] == foldid]
    controlTrain = [control[user] for user in controlUserFoldDict if controlUserFoldDict[user] != foldid]
    schTest = [sch[user] for user in schUserFoldDict if schUserFoldDict[user] == foldid]
    schTrain = [sch[user] for user in schUserFoldDict if schUserFoldDict[user] != foldid]
    
    XTrain = controlTrain + schTrain
    YTrain = [1]*len(controlTrain) + [0]*len(schTrain)
    [meanFt, varFt] = normFeatParams(XTrain)  #both meanFt and varFt are of length = numberoffeatures
    
    
    XTrain = normFeat(XTrain, meanFt, varFt)
    #TODO: SHUFFLE UP THE INPUT
    
    clf = svm.SVC()
    clf.fit(XTrain, YTrain)
    
    XTest = controlTest + schTest; XTest = normFeat(XTest, meanFt, varFt)
    YTest = [1]*len(controlTest) + [0]*len(schTest)
    preds = clf.predict(XTest)
    acc = getAccuracy(YTest, preds)
    print acc
    accuracy += [acc]
    
print 'mean accuracy', np.mean(accuracy)

"""
0.633333333333
0.642857142857
0.785714285714
0.642857142857
0.785714285714
0.678571428571
0.714285714286
0.807692307692
0.807692307692
0.75
mean accuracy 0.724871794872
"""
    
    


