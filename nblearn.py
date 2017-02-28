'''output text format: word truthful deceptive pos neg'''
import itertools
import re
import sys

def updateList(word, wordMap, wordList, label):
    
    if wordMap.get(word) == None:
        wordMap.update({word:len(wordMap)})
        
        templist = []
        for num in range(0, 4):
            templist.append(0)
        if label == "truthful":
            templist[0] += 1
        if label == "deceptive":
            templist[1] += 1
        if label == "positive":
            templist[2] += 1
        if label == "negative":
            templist[3] += 1
        wordList.append(templist)
    else:
        list = wordList[wordMap.get(word)]
        if label == "truthful":
            list[0] += 1
        if label == "deceptive":
            list[1] += 1
        if label == "positive":
            list[2] += 1
        if label == "negative":
            list[3] += 1
            
'''
trainFile = open("train-text.txt", 'r')
labelFile = open("train-labels.txt", 'r')
'''
trainFile = open(sys.argv[1], 'r')
labelFile = open(sys.argv[2], 'r')


'''first line would be probability for true false pos neg'''
modelFile = open("nbmodel.txt", 'w+')

cntT = 0
cntF = 0
cntP = 0
cntN = 0

wordMap = {}
wordList = []

for lineLabel, lineText in itertools.izip(labelFile, trainFile):
    lineLabel = lineLabel.replace("\n", "").replace("\r", "")
    labels = lineLabel.split(" ")
    lineText = lineText.replace("\n", " ").replace("-", " ").replace("/", " ").replace("?", " ").replace("\""," ").replace(";", " ").replace(":"," ").replace(",", " ").replace(".", " ").replace("\'", " ").replace("(", " ").replace(")", " ").replace("!", " ")
    text = lineText.split(" ")
    if labels[1] == "truthful":
        cntT += 1
    else:
        cntF += 1
    if labels[2] == "positive":
        cntP += 1
    else:
        cntN += 1

    for idxWord, word in enumerate(text):
        if idxWord > 0:
            for idxL, label in enumerate(labels):
                if idxL > 0 and len(word) > 0:
                    updateList(word.lower(), wordMap, wordList, label)
                    
modelFile.write(str(cntT*1.0/(cntT+cntF))+" "+str(cntF*1.0/(cntT+cntF))+" "+str(cntP*1.0/(cntT+cntF))+" "+str(cntN*1.0/(cntT+cntF))+"\n")
for item in wordMap:
    output = item
    '''output smoothed probablility, should filter the word with few counts'''
    list = wordList[wordMap[item]]
    cntNum = list[0] + list[1]
    probT = (list[0] + 1.00)/(cntNum + 2.00)
    probF = (list[1] + 1.00)/(cntNum + 2.00)
    probP = (list[2] + 1.00)/(cntNum + 2.00)
    probN = (list[3] + 1.00)/(cntNum + 2.00)
    output += " "+'%.3f' % probT + " "+'%.3f' % probF + " "+'%.3f' % probP + " "+'%.3f' % probN
    
    '''may need more filter here'''
    if cntNum < (cntT+cntF)/10 and cntNum > 1:
        modelFile.write(output+"\n")

