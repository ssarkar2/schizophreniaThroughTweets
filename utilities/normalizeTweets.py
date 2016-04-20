from utilities.ark_tweet_nlp_0_3_2.ark_tweet_nlp_python.CMUTweetTagger import *

def normTweet(x):
    RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar utilities/ark_tweet_nlp_0_3_2/ark-tweet-nlp-0.3.2.jar"
    print "Checking that we can see \"%s\", this will crash if we can't" % (RUN_TAGGER_CMD)
    success = check_script_is_present(RUN_TAGGER_CMD)
    if success:
        print "Success."
        print "Now pass in two messages, get a list of tuples back:"
        tweets = ['this is a message', 'and a second message']
        print runtagger_parse(tweets, run_tagger_cmd=RUN_TAGGER_CMD)
    


