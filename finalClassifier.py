import csv
from utilities.readTweet import readCSV
from sklearn import svm
import numpy as np
import theano
import theano.tensor as T
import lasagne, pydot
from sklearn.metrics import f1_score
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


def build_mlp(inpSize, input_var=None):
    l_in = lasagne.layers.InputLayer(shape=(None,inpSize), input_var=input_var)
    l_hid1 = lasagne.layers.DenseLayer(l_in, num_units=75, nonlinearity=lasagne.nonlinearities.sigmoid, W=lasagne.init.GlorotUniform())
    #l_hid2 = lasagne.layers.DenseLayer(l_hid1, num_units=10, nonlinearity=lasagne.nonlinearities.sigmoid)
    l_out = lasagne.layers.DenseLayer(l_hid1, num_units=1, nonlinearity=lasagne.nonlinearities.sigmoid)
    return l_out

def initNetwork(numFeatures):
    input_var = T.matrix('inputs')
    target_var = T.ivector('targets')
    network = build_mlp(numFeatures, input_var)
    prediction = T.transpose(lasagne.layers.get_output(network))
    loss = lasagne.objectives.squared_error(prediction, target_var)
    loss = loss.mean()
    params = lasagne.layers.get_all_params(network, trainable=True)
    updates = lasagne.updates.nesterov_momentum(loss, params, learning_rate=0.01, momentum=0.9)
    train_fn = theano.function([input_var, target_var], loss, updates=updates, allow_input_downcast=True)
    test_prediction = T.transpose(lasagne.layers.get_output(network, deterministic=True))
    test_acc = T.mean(T.eq(test_prediction > 0.5, target_var), dtype=theano.config.floatX)
    test_loss = lasagne.objectives.squared_error(test_prediction, target_var)
    val_fn = theano.function([input_var, target_var], [test_loss, test_acc, test_prediction], allow_input_downcast=True)
    #theano.printing.pydotprint(train_fn, 'pic.png', var_with_name_simple = True)
    return [train_fn, val_fn]

def findCutoff(pred, Y, inc):
    idealTh = []; maxMatch = -1
    for th in np.arange(0,1,inc):
        predTh = (pred>th)[0]
        matches = sum([1 if ((Y[i]==1 and predTh[i]==True) or (Y[i]==0 and predTh[i]==False)) else 0  for i in range(len(Y))])
        if maxMatch <= matches:
            if maxMatch == matches:
                idealTh += [th]
            else:
                idealTh = [th]
                maxMatch = matches
    return (max(idealTh)+min(idealTh))/2.

def findCorrelation(XTrain):
    t = np.asarray(XTrain)
    t = [[abs(pearsonr(t[:,featureId1], t[:,featureId2])[0]) for featureId2 in xrange(t.shape[1])] for featureId1 in xrange(t.shape[1])]
    plt.pcolor(t,cmap=plt.cm.Reds); plt.show(); plt.close()


def getFold(featureDict, userFoldDict, foldid, cond):
    return [featureDict[user] for user in userFoldDict if cond(userFoldDict[user], foldid)]

def findAccuracyF1MLP(pred, Y, th):
    predTh = (pred>th)[0]
    return [sum([1 if ((Y[i]==1 and predTh[i]==True) or (Y[i]==0 and predTh[i]==False)) else 0  for i in range(len(Y))])/(len(YTest)+0.),  f1_score(Y, [1 if i == True else False for i in predTh])]

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

def retainPerc(sortedList, perc = 0.99):
    t = np.cumsum(sortedList)
    for i in range(len(t)):
        if t[i] >= perc: return i
    return len(sortedList)

#this file is written assuming that there are 2 csvs for each feature (control and sch)
csvList = [['control_favorite_count.csv', 'control_simpleconnotation_features.csv', 'control_user_favourites_count.csv', 'control_user_followers_count.csv', 'control_user_friends_count.csv', 'control_user_statuses_count.csv', 'emoticonFeaturesCtrl.csv', 'RhymeFeaturesCtrl.csv', 'RhymeFeaturesCtrl1.csv', 'control_simplesentimentAFINN_features.csv'],   #, 'FrazierControl.csv', 'YngveControl.csv'], 
           ['sch_favorite_count.csv', 'sch_simpleconnotation_features.csv', 'sch_user_favourites_count.csv', 'sch_user_followers_count.csv', 'sch_user_friends_count.csv', 'sch_user_statuses_count.csv', 'emoticonFeaturesSch.csv', 'RhymeFeaturesSch.csv', 'RhymeFeaturesSch1.csv', 'sch_simplesentimentAFINN_features.csv']]   #, 'FrazierSch.csv', 'YngveSch.csv']]

useFeatures = {'control_favorite_count.csv':[0,0,1,0,1], 'sch_favorite_count.csv':[0,0,1,0,1],
                'control_simpleconnotation_features.csv':[1,1,1,1,1,1,0], 'sch_simpleconnotation_features.csv':[1,1,1,1,1,1,0],
                'control_user_favourites_count.csv':[1,0,1,1,0], 'sch_user_favourites_count.csv':[1,0,1,1,0],
                'control_user_followers_count.csv':[0,0,0,0,0], 'sch_user_followers_count.csv':[0,0,0,0,0],
                'control_user_friends_count.csv':[0,0,0,0,0], 'sch_user_friends_count.csv':[0,0,0,0,0],
                'control_user_statuses_count.csv':[1,0,1,1,0], 'sch_user_statuses_count.csv':[1,0,1,1,0],
                'emoticonFeaturesCtrl.csv':[1,0,1,1,0], 'emoticonFeaturesSch.csv':[1,0,1,1,0],
                'RhymeFeaturesCtrl.csv':[1]*4, 'RhymeFeaturesSch.csv':[1]*4,
                'RhymeFeaturesCtrl1.csv':[1]*4, 'RhymeFeaturesSch1.csv':[1]*4,
                #'control_simplesentimentAFINN_features.csv':[0]*11+[1,0,1,0], 'sch_simplesentimentAFINN_features.csv':[0]*11+[1,0,1,0]
                'control_simplesentimentAFINN_features.csv':[0]*15, 'sch_simplesentimentAFINN_features.csv':[0]*15,
                'FrazierControl.csv':[1]*8, 'FrazierSch.csv':[1]*8,
                'YngveControl.csv':[1]*8, 'YngveSch.csv':[1]*8
               }
#using only AFINN features
#csvList = [['control_simplesentimentAFINN_features.csv'], ['sch_simplesentimentAFINN_features.csv']]
#useFeatures = {'control_simplesentimentAFINN_features.csv':[0]+[1]*14, 'sch_simplesentimentAFINN_features.csv':[0]+[1]*14}

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
#print controlUserFoldDict

numFeatures = len(control[control.keys()[0]])
accuracySVM = []; accuracyMLP = []; accuracyADA = []
f1SVM = []; f1MLP = []; f1ADA = []
num_epochs = 5000
doPCA = False
for foldid in range(10):
    controlTest = getFold(control, controlUserFoldDict, foldid, lambda x,y:x==y)
    controlTrain = getFold(control, controlUserFoldDict, foldid, lambda x,y:x!=y)
    schTest = getFold(sch, schUserFoldDict, foldid, lambda x,y:x==y)
    schTrain = getFold(sch, schUserFoldDict, foldid, lambda x,y:x!=y)

    XTrain = controlTrain + schTrain
    YTrain = [1]*len(controlTrain) + [0]*len(schTrain)

    #findCorrelation(XTrain)  #plots graph of feature correlations

    #[meanFt, varFt] = normFeatParams(XTrain)  #both meanFt and varFt are of length = numberoffeatures
    #XTrain = normFeat(XTrain, meanFt, varFt)

    PCAObject = PCA(np.asarray(XTrain))

    XTrain = PCAObject.center(XTrain)
    if doPCA:
        numFeatures =  retainPerc(PCAObject.fracs, 0.99)
        XTrain = PCAObject.project(XTrain)[:,0:numFeatures]
        [meanFt, varFt] = normFeatParams(XTrain)  #both meanFt and varFt are of length = numberoffeatures
        XTrain = np.asarray(normFeat(XTrain, meanFt, varFt))
        #print numFeatures, XTrain.shape

    #TODO: SHUFFLE UP THE INPUT

    clf = svm.SVC(kernel='rbf')
    clf.fit(XTrain, YTrain)

    XTest = controlTest + schTest
    XTest = PCAObject.center(XTest)
    if doPCA:
        XTest = PCAObject.project(XTest)[:,0:numFeatures]
        XTest = np.asarray(normFeat(XTest, meanFt, varFt))

    YTest = [1]*len(controlTest) + [0]*len(schTest)
    preds = clf.predict(XTest)
    acc = getAccuracy(YTest, preds)
    #print preds, acc

    accuracySVM += [acc]
    f1SVM += [f1_score(YTest, preds)]


    #MLP
    [train_fn, val_fn] = initNetwork(numFeatures)
    for epoch in range(num_epochs):
        #print np.asarray(XTrain).shape, np.asarray(YTrain).shape, numFeatures, epoch
        train_err = train_fn(np.asarray(XTrain), np.asarray(YTrain))
        #print train_err,
    err, accN, pred = val_fn(np.asarray(XTrain), np.asarray(YTrain))
    th = findCutoff(pred, YTrain, 0.01)
    err, accN, pred = val_fn(np.asarray(XTest), np.asarray(YTest))
    [accN,f1] = findAccuracyF1MLP(pred, YTest, th)
    #print err,acc,pred, 'NN'
    accuracyMLP += [accN]
    f1MLP += [f1]
    
    
    #adaboost
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=5), algorithm="SAMME", n_estimators=700)
    bdt.fit(XTrain, YTrain)
    predADA = bdt.predict(XTest)
    accADA = getAccuracy(YTest, predADA)
    accuracyADA += [accADA]
    f1ADA += [f1_score(YTest, predADA)]
    

    print foldid, 'SVM', acc, 'MLP', accN, 'ADA', accADA


print 'mean accuracy SVM', np.mean(accuracySVM)
print 'mean accuracy MLP', np.mean(accuracyMLP)
print 'mean accuracy ADA', np.mean(accuracyADA)
print 'mean F1 SVM', np.mean(f1SVM)
print 'mean F1 MLP', np.mean(f1MLP)
print 'mean F1 ADA', np.mean(f1ADA)


"""
0 SVM 0.633333333333 MLP 0.600000023842
1 SVM 0.642857142857 MLP 0.714285731316
2 SVM 0.785714285714 MLP 0.821428596973
3 SVM 0.642857142857 MLP 0.75
4 SVM 0.785714285714 MLP 0.678571403027
5 SVM 0.678571428571 MLP 0.75
6 SVM 0.714285714286 MLP 0.642857134342
7 SVM 0.807692307692 MLP 0.807692289352
8 SVM 0.807692307692 MLP 0.807692289352
9 SVM 0.75 MLP 0.666666686535
mean accuracy SVM 0.724871794872
mean accuracy MLP 0.723919
"""
