import sys
import json
import io
import os

CMU_TWEET = "../../utilities/ark_tweet_nlp_0_3_2"

sys.path.append(os.path.join(CMU_TWEET, "ark_tweet_nlp_python"))

import CMUTweetTagger 

inp = sys.argv[1]
DATA = sys.argv[2]

tweets = []
with open(os.path.join(DATA, inp), "r") as f:
    for i, line in enumerate(f):
        fields = line.rstrip("\n").split("\t")
        tweets.append(fields[3].decode("utf-8"))
    
tweets_parsed = CMUTweetTagger.runtagger_parse(tweets, 
                run_tagger_cmd="java -XX:ParallelGCThreads=2 -Xmx500m -jar " + os.path.join(CMU_TWEET, "ark-tweet-nlp-0.3.2.jar"))
data = []

with io.open(os.path.join(DATA, inp + ".proc"), "w", encoding="utf-8") as w:
    with open(os.path.join(DATA, inp), "r") as f:
        for i, line in enumerate(f):
            fields = line.rstrip("\n").split("\t")
            instance = {}
            instance["tweetid"] = fields[0]
            instance["userid"] = fields[1]
            instance["sentiment"] = fields[2]
            instance["tweet"] = [e[0].decode("utf-8") for e in tweets_parsed[i]]
            instance["pos"] = [e[1] for e in tweets_parsed[i]]
            data.append(unicode(json.dumps(instance, sort_keys=True, ensure_ascii=False)))
    print len(data)
    w.write(u"[\n" + ",\n".join(data) + u"\n]")

json.loads(open(os.path.join(DATA, inp + ".proc"), "r").read())
