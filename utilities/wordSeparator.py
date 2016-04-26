#http://stackoverflow.com/questions/20516100/term-split-by-hashtag-of-multiple-words
#separates out words that are not space separated. Takes hints from caps, follows a greedy strategy

def InitializeWords(wordlist):
    content = None
    with open(wordlist) as f:
        content = f.readlines()
    return [word.rstrip('\n') for word in content]

def insertDashBeforeCaps(term):
    #insert - before Caps letters if they dont have caps ahead of them. so awesomeDay -> awesome-Day. but IBM -> IBM
    #Also if there is a bunch of caps, insert a - before the last in the bunch. eg helloWorldIBMRocks -> hello-World-IBM-Rocks   (note wont work for )  helloWorldIBMrocks
    newterm = ''; capsRun = 0
    for idx in xrange(0, len(term)):
        if term[idx].isupper():
            capsRun = capsRun + 1
            if idx != 0:  #if the first letter is caps, dont add caps
                if term[idx-1].islower():
                    newterm += '-'
                if term[idx-1].isupper() and capsRun > 1:
                    if idx != len(term) - 1: #if the caps letter isnt the last letter
                        if term[idx+1].islower():
                            newterm += '-'
        else:
            capsRun = 0
        newterm += term[idx]
    return newterm

def parseTagSingleWord(term):
    wordlisttxt = 'utilities/englishWords.txt' # A file containing common english words  #assumes we are running from the top directory (schizophreniaThroughTweets)
    wordlist = InitializeWords(wordlisttxt)
    words = []
    # Remove hashtag,
    if term[0] == '#':
        term = term[1:]
    if term.isupper():  #everything is caps, so no information comes from caps. so lowercasing everything
        term = term.lower()
    term = insertDashBeforeCaps(term)
    #split by dash
    tags = term.split('-')
    for tag in tags:
        if tag.isupper():  #if all letters are caps, just retain the word
            if tag.lower() in wordlist: #lowercase the word if it is present in the word list
                word = tag.lower()
            else:
                word = tag
        else:
            word = FindWord(tag, wordlist)
        while word != None and len(tag) > 0:
            words += [word]
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = FindWord(tag, wordlist)
    return " ".join(words)

def FindWord(token, wordlist):  #longest match
    i = len(token) + 1
    while i > 1:
        i -= 1
        if token[:i].lower() in wordlist:
            return token[:i].lower()
    return token #if no match is found just return the whole thing

def parseTag(term):  #term can be a list or a single string
    if type(term) is str:
        term = [term]  #convert to list form (singleton list)
    return [parseTagSingleWord(t) for t in term]


#TESTING HASHTAG SPLITTER
'''
sentence = "big #awesome-dayofmylife because #iamgreat"
print parseTag('#iamgreat')
print parseTag(['#HelloWorldIBMrocks', '#HelloWorldIBMRocks', 'helloWorldFLYYouFool', 'wywyywywyw'])
print insertDashBeforeCaps('helloWorld') #hello-World
print insertDashBeforeCaps('helloWorldIBM') #hello-World-IBM
print insertDashBeforeCaps('helloWorldIBMwow')  #hello-World-IB-Mwow
print insertDashBeforeCaps('HelloWorldIBMWow') #Hello-World-IBM-Wow
print insertDashBeforeCaps('HelloWorld-IBMWow') #Hello-World-IBM-Wow
print insertDashBeforeCaps('IBMrocks')  #IB-Mrocks
'''