DATA=../data
TRAIN=tweets.2013.train
TEST=tweets.2013.dev

TRAIN_PROC=${TRAIN}.proc
TEST_PROC=${TEST}.proc

if [ ! -f $DATA/$TRAIN_PROC ]; then
        python tokenize-tag-data.py $TRAIN $DATA
fi

if [ ! -f $DATA/$TEST_PROC ]; then
        python tokenize-tag-data.py $TEST $DATA
fi

TRAIN_VW=$DATA/${TRAIN_PROC}.${1}.vw
TEST_VW=$DATA/${TEST_PROC}.${1}.vw

# Remove old files
rm -rf $TRAIN_VW $TEST_VW

# Extract features
python vw_make_data.py ${TRAIN_PROC} $1 $DATA
python vw_make_data.py ${TEST_PROC} $1 $DATA

# Train model
vw --csoaa 3 -d $TRAIN_VW --passes 20 -c -k -f models/${1}.model --early_terminate 999 -b 24 --l1 0.000001

# Predict 
PREDICT_TMP=${TEST}.${1}.pred 
vw -t -i models/${1}.model -p $PREDICT_TMP $TEST_VW

python make-pred-file.py $PREDICT_TMP $DATA/$TEST

printf "\n"

PREDICT=$DATA/${TEST}.pred
perl scorer.pl $DATA/$TEST $PREDICT

# Clean up
rm -rf $PREDICT_TMP 
rm $DATA/*.cache
