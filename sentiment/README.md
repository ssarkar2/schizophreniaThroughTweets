This folder contains code and data for training a Tweet sentiment detector. 

# 1. Training:

Install vowpal-wabbit: https://github.com/JohnLangford/vowpal_wabbit

Go to "train.sh", change variables "TRAIN" and "TEST" to the train and test files, respectively.

Run:

> ./train.sh [model_name]

"model_name" can be any name. Example:

> ./train.sh bigram

# 2. Data:

*DO NOT PUBLISH OR RE-DISTRIBUTE DATA ON THIS DIRECTORY (according to Twitter's policies).*

Collect from SemEval 2013/2014/2015/2016 sentiment analysis task. The data is not complete because some tweets have been deleted by users. 

Datasets:

+ Tweets 2013 (train + dev + test)
+ Tweets 2014 (test + sacarsm)
+ Tweets 2016 (test + dev + devtest)
+ SMS 2013 
+ Live Journal 2014

TODO: if have Tweets 2015 (test), please add.

See: http://alt.qcri.org/semeval2016/task4/data/uploads/semeval2016_task4_report.pdf
