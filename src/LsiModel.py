from gensim import corpora, models, similarities
import gensim
import logging

class LsiModel:
    def __init__(self,corpusManipulator):
        self.corpusTimeStamp=corpusManipulator.corpusTimeStamp
        self.corpusManipulator=corpusManipulator
        self.dictionary=corpusManipulator.dictionary
        self.corpus=corpusManipulator.getCorpus()
        self.lsiModel=models.LsiModel(corpusManipulator.getCorpus(), id2word=corpusManipulator.dictionary, num_topics=256)
        self.reindex()
        #self.indexing=similarities.MatrixSimilarity(self.lsiModel[corpusManipulator.corpus])
    def isModelUpdated(self):
        return self.corpusTimeStamp==self.corpusManipulator.corpusTimeStamp
    def versionProcceed(self):
        self.corpusTimeStamp=self.corpusManipulator.corpusTimeStamp
    def addDocuments(self,corpus):#add documents to Lsi Model
        self.lsiModel.add_documents(corpus)
        self.reindex()
        '''if self.isModelUpdated():
            self.lsiModel.add_documents(self.corpusManipulator.corpus)
        if not self.isModelUpdated():
            self.oldModel=self.lsiModel
            self.lsiModel.id2word=self.corpusManipulator.dictionary
            self.lsiModel.add_documents(self.corpusManipulator.corpus)'''
        #self.lsiModel=models.LsiModel(self.corpusManipulator.corpus, id2word=self.corpusManipulator.dictionary, num_topics=256)
            
    def reindex(self):#reindexing similarity matrix
        self.indexing=similarities.MatrixSimilarity(self.lsiModel[self.corpusManipulator.getCorpus()])
    def batchPredict(self,idVecs):
        return [self.predict(i) for i in idVecs]
    def predict(self,idVec):
        #print(idVec)
        lsiModel=self.lsiModel #if self.isModelUpdated() else self.oldModel
        idVec=lsiModel[idVec]
        sims = self.indexing[idVec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims
    def saveProfile(self):
        #self.dictionary.save('')
        return 0