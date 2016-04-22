# -*- coding: utf-8 -*-
import TweeboParser

tweets = [u"Word I'm bout to holla at her via twitter RT @iamJay_Fresh : #trushit - im tryna fucc nicki minaj lol", 
          u"To appear (EMNLP 2014): Detecting Non-compositional MWE Components using Wiktionary http://people.eng.unimelb.edu.au/tbaldwin/pubs/emnlp2014-mwe.pdf … #nlproc"]

print TweeboParser.parse(tweets)


