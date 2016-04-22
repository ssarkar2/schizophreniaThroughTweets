DATA=../data
TRAIN=2013.train
TEST=2013.dev


TRAIN_DATA=$DATA/tweets.vw.${1}.${TRAIN}
TEST_DATA=$DATA/tweets.vw.${1}.${TEST}

# Remove old files
rm -rf $TRAIN_DATA $TEST_DATA

# Extract features
python vw_make_data.py $TRAIN $1 $DATA
python vw_make_data.py $TEST $1 $DATA

# Train model
PREDICT=tweets.vw.${1}.${TEST}.pred 
vw --csoaa 3 -d $TRAIN_DATA --passes 20 -c -k -f models/${1}.model --early_terminate 999 -b 24 --l1 0.000001
vw -t -i models/${1}.model -p $PREDICT $TEST_DATA

GOLD=$DATA/tweets.${TEST}
python make-pred-file.py $PREDICT $GOLD
rm -rf $PREDICT 

printf "\n"

OUTPUT=$DATA/tweets.${TEST}.pred
perl scorer.pl $GOLD $OUTPUT
