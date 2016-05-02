from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from utilities.twokenize import tokenize
import numpy as np
import pandas as pd
import gzip
import glob
import json
import codecs
import sys

reader = codecs.getreader("utf-8")


def read_corpus(inputDir):
    '''
    Reads tweets text from compressed files and returns a dict of user
    and their tweets. Dict format:
    key : user_id
    value: list of tweets
    '''
    corpus = {}
    for filename in glob.glob(inputDir+'/*.gz'):
        user_id = filename.split('/')[-1].split('.')[0]
        user_tweets_text = []
        with gzip.open(filename, 'rb') as f:
            for line in reader(f):
                line = line.replace('\n','')
                text_json = json.loads(line)['text']
                user_tweets_text.append(text_json)
        corpus[user_id] = user_tweets_text
    return corpus


def nltk_tokenize(text):
    tokens = word_tokenize(text)
    return tokens


def tweet_tokenizer(text, cleanup = 0):  #cleanup = 3 is suggested
    #tokens = tokenize(text)
    #return tokens
    return tokenize(text, cleanup)


def get_train_test_split_text_features(k, k_fold_features, k_fold_labels):
    X_train = sum(k_fold_features[:k]+k_fold_features[k+1:],[])
    Y_train = sum(k_fold_labels[:k]+k_fold_labels[k+1:], [])
    X_test= k_fold_features[k]
    Y_test = k_fold_labels[k]
    return X_train, Y_train, X_test, Y_test


def generate_k_fold_split(file_path):
    reference_df = pd.read_csv(file_path)
    reference_df = reference_df.set_index('anonymized_name')
    return {k:reference_df[reference_df['fold']==k].index.tolist() for k in range(10)}


def get_text_features(k_folds_users_split, control_corpus, sch_corpus):
    k_fold_features = []
    k_fold_labels = []
    for k in range(10):
        users = k_folds_users_split[k]
        features = []
        labels = []
        for user in users:
            if user in control_corpus.keys():
                features.append(' '.join(control_corpus[user]))
                labels.append(0)
            elif user in sch_corpus.keys():
                features.append(' '.join(sch_corpus[user]))
                labels.append(1)
        k_fold_features.append(features)
        k_fold_labels.append(labels)
    return k_fold_features, k_fold_labels


def get_train_test_split_non_text_features(k, k_folds_users_split, features_df):
    k_fold_users = [k_folds_users_split[i] for i in range(10)]
    train_users = sum(k_fold_users[:k]+k_fold_users[k+1:],[])
    test_users = k_fold_users[k]
    train_df = features_df.ix[train_users]
    test_df = features_df.ix[test_users]
    return train_df, test_df



if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("provide anonymized_control_tweets folder path, anonymized_schizophrenia_tweets folder path "\
              "anonymized_user_manifest.csv path and normalized_sch_liwc_count.csv path")
        print("Example: python unigram_logit_classifier.py anonymized_control_tweets "\
              "anonymized_schizophrenia_tweets anonymized_user_manifest.csv normalized_sch_liwc_count.csv")
        sys.exit()

    control_folder_path = sys.argv[1]
    sch_folder_path = sys.argv[2]
    reference_file_path = sys.argv[3]
    liwc_file_path = sys.argv[4]

    control_corpus_dict = read_corpus(control_folder_path)
    sch_corpus_dict = read_corpus(sch_folder_path)
    k_folds_users_split = generate_k_fold_split(reference_file_path)
    k_fold_text_features, k_fold_labels = get_text_features(k_folds_users_split, control_corpus_dict, sch_corpus_dict)

    liwc_count_df = pd.read_csv(liwc_file_path)
    liwc_count_df.set_index('Unnamed: 0', inplace=True)

    scores = []
    print ('Precision, Recall , F1-score')
    for k in range(10):
        X_train, y_train, X_test, y_test = get_train_test_split_text_features(k, k_fold_text_features, k_fold_labels)
        # discard all tokens which are present in more than 50% tweets or in less than 5 tweets.
        vectorize = TfidfVectorizer(tokenizer= tweet_tokenizer, ngram_range=(1, 1), binary=True, max_features=1000,
                                     min_df=5, max_df= 0.50)
        train_data_features = vectorize.fit_transform(X_train)
        test_data_features = vectorize.transform(X_test)

        #generate liwc features
        train_df, test_df = get_train_test_split_non_text_features(k, k_folds_users_split, liwc_count_df)

        #append unigram and liwc features.
        train_data_features = np.hstack([train_data_features.todense(), train_df])
        test_data_features = np.hstack([test_data_features.todense(), test_df])

        clf = LogisticRegression()
        clf.fit(train_data_features, y_train)
        predicted_values = clf.predict(test_data_features)
        scr = precision_recall_fscore_support(y_test, predicted_values, average='binary')
        print (scr)
        scores.append(scr)
    print('Mean F-1 score')
    print (np.mean([s[2] for s in scores]))