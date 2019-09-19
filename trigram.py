import random


"""
Bigram Links list
"""
class BiNode:
    def __init__(self, biWord, triWord): #[ biWord | nextBi | triWord]
        self.biWord = biWord
        self.nextBi = None
        self.triWord = TriNode(triWord)

"""
Trigram Links list
"""
class TriNode:
    def __init__(self, triWord): #[ triWord | count | pointer to next tri]
        self.triWord = triWord
        self.triCount = 1
        self.nextTri = None
        
        

"""
Convert a story text file to a list of words to use.
Converts all words to lowercase
Params: text - the text to be converted
Return: words - list of individual words.
"""
def storyToListOfWords(text):
    text = open(text, "r")
    words = []
    for line in text:
        for word in line.split():
            words.append(word.lower())
    return words

"""
Makes trigrams with dictionary/linked list helpers.
Params: words - story in list form
Return: trigram in dictionary/linked list 
"""
def makeTrigrams(words, dic):
    for i in range(0, len(words) - 2):  
        word = words[i]
        if word in dic:
            bigramNode = dic[word] #bigram pointer [word[i-1] | word[i-2]]
            checkBigrams(words, i, bigramNode)     
        #not in dict
        else:
            dic[word] = BiNode(words[i+1], words[i+2]) #make new Bigram link
    return dic

"""
Will check bigrams and call trigrams checker
Params:
    words: story
    i: position of current word
    bigramNode: current bigram link
"""
def checkBigrams(words, i, bigramNode):
    found = False
    while(True):
        if words[i + 1] == bigramNode.biWord:
            found = True
            trigramNode = bigramNode.triWord
            checkTrigrams(words, i, trigramNode)
            break
        elif bigramNode.nextBi == None:
            break
        bigramNode = bigramNode.nextBi

    #make nextBi link since not in yet
    if (found == False):
        bigramNode.nextBi = BiNode(words[i + 1], words[i + 2])


"""
Checks the trigrams portion of link
Params:
    words: the story
    i: position of word in story
    triNode: the tri link
"""
def checkTrigrams(words, i, triNode):
    while(True):
        if words[i+2] == triNode.triWord:
            triNode.triCount += 1
            return
        elif triNode.nextTri == None:
            break
        triNode = triNode.nextTri

    #make nextTrilink if not found
    triNode.nextTri = TriNode(words[i+2])

"""
Method to test the trigrams output
"""
def outputTrigrams(trigrams):
    outFile = open("bigramsOut.txt", "w")
    for item,v in trigrams.items():
        out = "FIRST WORD: {}: \n".format(item)
        out += "-" *40 + "\n"
        p = v
        while(p != None):
            out += "{}, ".format(p.biWord)
            t = p.triWord
            out += "[TRIWORDS: {}:{} ".format(t.triWord.upper(), t.triCount)
            t = t.nextTri
            while(t != None):
                out += "{}:{} ".format(t.triWord.upper(), t.triCount)
                t = t.nextTri
            out+= "] \n\n"
            p = p.nextBi
        out += ")\n\n\n\n\n"
        outFile.write(out)

"""
Make trigrams dic with multiple stories
Params:
    stories: list of stories
Return:
    dictionary of stories trigrams
"""
def makeDicFromMultipleStories(stories):
    dic = {}
    for i in stories:
        storyList = storyToListOfWords(i)
        makeTrigrams(storyList, dic)
    return dic

"""
Generate 1000 words of text using given dictionary
        return list of words
Params:
    dic
"""
def generateText(dic):
    genWords = [] #empty
    while(len(genWords) < 1000):
        word1, word2 = random.choice(list(dic.items())) #string, BiNode
        word2 = chooseRandomLink(word2) #binode object
        word3 = chooseRandomByProportion(word2.triWord, dic)
        genWords.append(word1)
        genWords.append(word2.biWord)
        genWords.append(word3)
    return genWords

"""
Use triword link to choose next word.
Uses proportions
Params:
    triword - triword link
    dic - for specifying biNode object
Return
    randomly chosen word
"""
def chooseRandomByProportion(triWord, dic):
    myList = []
    p = triWord
    for i in range(triWord.triCount):
        myList.append(triWord)
    while(p.nextTri != None):
        for i in range(triWord.triCount):
            myList.append(triWord)
        p = p.nextTri
    return(random.choice(myList).triWord)

def chooseRandomLink(biGramNode):
    p = biGramNode
    myList = []
    myList.append(p)
    while(p.nextBi != None):
        p = p.nextBi
        myList.append(p)
    return(random.choice(myList))
def main():
    holmesTexts = ["doyle-27.txt", "doyle-case-27.txt"]
    allTexts = ["alice-27.txt", ]
   
    holmesTrigrams = makeDicFromMultipleStories(holmesTexts)
    r = open("holmesRandom.txt", "w")
    g = generateText(holmesTrigrams)
    out = " ".join(g)
    r.writelines(out)

    allTrigrams = makeDicFromMultipleStories(allTexts)
    b = open("allRandom.txt", "w")
    g = generateText(holmesTrigrams)
    out = " ".join(g)
    b.writelines(out)

    r.close()
    b.close()
if __name__ == '__main__':
    main()
