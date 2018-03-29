from gensim import corpora

def removeDuplicate(myList,codeList):
    res=list()
    code=list()
    for x in range(len(myList)):
        if x not in res:
            res.append(myList[x])
            code.append(codeList[x])
    return [res, code]


class CorpusDataManipulator:
    def __init__(self,wordVecs,correspondingCodes):
        self.dictionary=corpora.Dictionary(wordVecs)
        self.corpus = [self.dictionary.doc2bow(x) for x in wordVecs]
        self.corpusWithoutDuplicate, self.codeWithoutDuplicate = removeDuplicate(self.corpus,correspondingCodes)
        #self.corpus = set(map(tuple,map(self.dictionary.doc2bow,wordVecs)))
        #print(self.corpus)
        self.corpusTimeStamp=0
        self.tokenAmount=len(self.dictionary.items())
    def stepForward(self):
        self.corpusTimeStamp+=1
            
    def addVecToDic(self,wordVecs):
        self.dictionary.add_documents(wordVecs)
        '''if len(self.dictionary.items())>self.tokenAmount:
            self.stepForward()'''
        #self.addVecToCorpus(self.doc2bow(wordVec))
    def doc2bow(self,wordVec):
        return self.dictionary.doc2bow(wordVec)
    def addVecToCorpus(self,idVecs,codes):
        #self.corpus.update(map(tuple(idVecs)))
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
        return 0