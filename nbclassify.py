import sys


def probWord(word, wordMap, wordList, label):
    if wordMap.get(word) == None:
        return 1.0
    else:
        list = wordList[wordMap.get(word)]
        if label == "truthful":
            return list[0]
        elif label == "deceptive":
            return list[1]
        elif label == "positive":
            return list[2]
        elif label == "negative":
            return list[3]
        else:
            return 0


testFile = open(sys.argv[1], 'r')
modelFile = open("nbmodel.txt", 'r')

predictFile = open("nboutput.txt", 'w+')
probT = 0.0
probF = 0.0
probP = 0.0
probN = 0.0
wordMap = {}
wordList = []

'''input model to wordMap and wordList'''
for idx, line in enumerate(modelFile):
    line = line.strip("\n")
    probData = line.split(" ")
    if idx == 0:
        probT = float(probData[0])
        probF = float(probData[1])
        probP = float(probData[2])
        probN = float(probData[3])
    else:
        wordMap.update({probData[0]:len(wordList)})
        list = []
        for prob in probData[1:]:
            list.append(float(prob))
        wordList.append(list)
    

for line in testFile:
    line = line.replace("\n", " ").replace("-", " ").replace("/", " ").replace("?", " ").replace("\""," ").replace(";", " ").replace(":"," ").replace(",", " ").replace(".", " ").replace("\'", " ").replace("(", " ").replace(")", " ").replace("!", " ")
    text = line.split(" ")
    tempT = probT
    tempF = probF
    tempP = probP
    tempN = probN
    output = ""
    for idx, word in enumerate(text):
        if idx > 0:
            tempT *= probWord(word.lower(), wordMap, wordList, "truthful")
            tempF *= probWord(word.lower(), wordMap, wordList, "deceptive")
            tempP *= probWord(word.lower(), wordMap, wordList, "positive")
            tempN *= probWord(word.lower(), wordMap, wordList, "negative")
        else:
            output += word
            

    if tempT > tempF:
        output += " truthful"
    else:
        output += " deceptive"
    if tempP > tempN:
        output += " positive"
    else:
        output += " negative"
    output += "\n"
    predictFile.write(output)
