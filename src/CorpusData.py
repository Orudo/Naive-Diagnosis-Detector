from gensim import corpora
import dataManipulator
import json
import logging
import time

def removeDuplicate(myList,codeList):
    res=list()
    code=list()
    for x in range(len(myList)):
        if x not in res:
            res.append(myList[x])
            code.append(codeList[x])
    return [res, code]


class CorpusDataManipulator:
    def __init__(self,wordVecs,correspondingCodes,loadFromFile):
        if loadFromFile:
            #self.dictionary=corpora.Dictionary()
            self.dictionary=corpora.Dictionary.load(dataManipulator.dataManipulator.conf["path"]["dictionary"])
            print(self.dictionary)
            #time.sleep(10)
            with open(dataManipulator.dataManipulator.conf["path"]["corpus"]) as f:
                self.corpusWithoutDuplicate=json.loads(f.readline())
                self.corpusWithoutDuplicate=list(map(lambda x:list(map(lambda y:tuple(y),x)),self.corpusWithoutDuplicate))
            with open(dataManipulator.dataManipulator.conf["path"]["codes"]) as f:
                self.codeWithoutDuplicate=json.loads(f.readline())
            
            self.tokenAmount=len(self.dictionary.items())
        else:
            self.dictionary=corpora.Dictionary(wordVecs)
            self.corpus = [self.dictionary.doc2bow(x) for x in wordVecs]
            self.corpusWithoutDuplicate, self.codeWithoutDuplicate = removeDuplicate(self.corpus,correspondingCodes)
            self.tokenAmount=len(self.dictionary.items())
        self.corpusTimeStamp=0
        #print(self.dictionary)
            
        #print(self.dictionary.id2token)
        #time.sleep(20)

    def stepForward(self):
        self.corpusTimeStamp+=1
            
    def addVecToDic(self,wordVecs):
        self.dictionary.add_documents(wordVecs)
    def doc2bow(self,wordVec):
        return self.dictionary.doc2bow(wordVec)
    def addVecToCorpus(self,idVecs,codes):
        idVecs, codes=removeDuplicate(idVecs,codes)
        datas=list(map(lambda x,y:[x,y],idVecs,codes))
        print(datas)
        datas=list(filter(lambda x:x[0] not in self.corpusWithoutDuplicate,datas))
        print(datas)
        self.corpusWithoutDuplicate.extend(list(map(lambda x:x[0],datas)))
        self.codeWithoutDuplicate.extend(list(map(lambda x:x[1],datas)))
        return list(map(lambda x:x[0],datas))
    def getText(self,docNo):
        return self.corpus[docNo]
    def bow2doc(self,text):
        return list(map(lambda x:self.dictionary.id2token[x],map(lambda x:x[0],text)))
    def getCode(self,docNo):
        return self.codeWithoutDuplicate[docNo]
    def getCorpus(self):
        return self.corpusWithoutDuplicate
    
    def saveCorpusAndCodes(self):
        self.dictionary.save(dataManipulator.dataManipulator.conf["path"]["dictionary"])
        with open(dataManipulator.dataManipulator.conf["path"]["corpus"],"w") as f:
            f.write(json.dumps(self.corpusWithoutDuplicate))
        with open(dataManipulator.dataManipulator.conf["path"]["codes"],"w") as f:
            f.write(json.dumps(self.codeWithoutDuplicate))
        logging.info("corpusinfoSaved")
        return 0