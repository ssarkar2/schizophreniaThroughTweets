import os, gzip

def createDir(dirname): #check if such a directory exists, else create a new one.
    try: os.stat(dirname)
    except: os.mkdir(dirname)

def unzipAll(sourceDir, targetDir):
    createDir(targetDir)
    for filename in os.listdir(sourceDir):     
        fout = open(targetDir + filename.split('.')[0] + '.txt', 'w')
        f = gzip.open(sourceDir + filename, 'rb')        
        fout.write(f.readline())
        
    
#note directories should end with '/' in the input arguments
#note extraction is not really required, you can just read off the gz files directly as is done in lines 11-12
unzipAll('/scratch0/sem4/cmsc773/data/data/clpsych2015/schizophrenia/anonymized_control_tweets/', '/scratch0/sem4/cmsc773/data/data/clpsych2015/schizophrenia/anonymized_control_tweets_unzipped/')