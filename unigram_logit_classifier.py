from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import f1_score
import numpy as np
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


# NLTK's tokenizer. We can use a better tokenizer later.
def tokenize(text):
    tokens = word_tokenize(text)
    return tokens


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("provide anonymized_control_tweets and anonymized_schizophrenia_tweets folders path.")
        print("Example: python unigram_logit_classifier.py anonymized_control_tweets anonymized_schizophrenia_tweets")
        sys.exit()
    control_folder_path = sys.argv[1]
    sch_folder_path = sys.argv[2]
    control_corpus_dict = read_corpus(control_folder_path)
    sch_corpus_dict = read_corpus(sch_folder_path)

    all_corpus_as_list = []
    labels = []
    for control, sch in zip(control_corpus_dict.values(), sch_corpus_dict.values()):
        all_corpus_as_list.append(' '.join(control))
        labels.append(-1)
        all_corpus_as_list.append(' '.join(sch))
        labels.append(1)

    skf = StratifiedKFold(labels, n_folds=5)
    scores = []
    for train_index, test_index in skf:
        X_train = [all_corpus_as_list[i] for i in train_index]
        y_train = [labels[i] for i in train_index]
        X_test = [all_corpus_as_list[i] for i in test_index]
        y_test = [labels[i] for i in test_index]
        # discard all tokens which are present in more than 50% tweets or in less than 5 tweets.
        vectorize = TfidfVectorizer(tokenizer=tokenize, ngram_range=(1, 1), binary=True, max_features=1000,
                                     min_df=5, max_df= 0.50)
        train_data_features = vectorize.fit_transform(X_train)
        test_data_features = vectorize.transform(X_test)
        clf = LogisticRegression()
        clf.fit(train_data_features, y_train)
        predicted_values = clf.predict(test_data_features)
        scores.append(f1_score(y_test, predicted_values, average='binary'))

print(scores)
print(np.mean(scores))