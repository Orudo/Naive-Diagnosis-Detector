from gensim import corpora

class CorpusDataManipulator:
    def __init__(self,wordVecs):
        self.dictionary=corpora.Dictionary(wordVecs)
        self.corpus = [self.dictionary.doc2bow(x) for x in wordVecs]
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
    def addVecToCorpus(self,idVecs):
        self.corpus.extend(idVecs)
