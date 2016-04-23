from collections import defaultdict
from utilities.twokenize import tokenize
import codecs

reader = codecs.getreader("utf-8")


def tweet_tokenizer(text):
    tokens = tokenize(text)
    return tokens


def read_liwc_dict(liwc_dict_path):
    liwc_cat_dict = {}
    liwc_word_dict = defaultdict(list)
    header = True
    with open(liwc_dict_path, 'rb') as f:
        for line in reader(f):
            if '%' in line or '/' in line:
                continue
            line = line.replace('\n','').strip()
            tokens = line.split('\t')
            if header:
                liwc_cat_dict[tokens[0]] = tokens[1]
                if '464\tfiller' in line:
                    header= False
            else:
                liwc_word_dict[tokens[0]] = [liwc_cat_dict[token] for token in tokens[1:]]

    return liwc_word_dict, liwc_cat_dict.values()


def count_liwc_cat(tweets, liwc_dict, liwc_cat):
    count_dict = {c:0 for c in liwc_cat}
    for tweet in tweets:
        tokens = set(tweet_tokenizer(tweet.lower()))
        for k in liwc_dict.keys():
            if '*' in k:
                for t in tokens:
                    if k[:-1] in t:
                        for c in liwc_dict[k]:
                            count_dict[c]+=1

            elif k in tokens:
                for c in liwc_dict[k]:
                    count_dict[c]+=1
    return count_dict

if __name__ =='__main__':
    liwc_dict_path = '../../LIWC2007_updated.dic'
    read_liwc_dict(liwc_dict_path)