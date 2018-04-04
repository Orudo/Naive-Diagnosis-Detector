from NLPUtilities import *
import LsiModel
import CorpusData
import TFIDFSplitter
import logging
import jieba
import time
from gensim.test.utils import get_tmpfile
import dataManipulator
import diagnosesData
import json
from pathlib import Path
import math
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class DiagInquryer:
    def confinit(self):
        jsonData=open("/home/martin/Naive-Diagnosis-Detector/data/Conf.json").read()
        conf=json.loads(jsonData)

        self.conf=conf

    def __init__(self):
        dMani=dataManipulator.dataManipulator
        jieba.load_userdict(dMani.conf["path"]["jiebaDic"])
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


        tmp_fname = get_tmpfile("lsi.model")
        indicator=Path(tmp_fname).exists()#dMani.conf["path"]["LsiModel"]).exists()
        if indicator:
            self.corpusMani=CorpusData.CorpusDataManipulator("","",indicator)
            self.lsi=LsiModel.LsiModel(self.corpusMani,indicator)
        else:
            trainingSet=json.loads(open(dMani.conf["path"]["trainingSet"]).read())
            self.codes=list(map(lambda x:x[1],trainingSet))
            contents=list(map(lambda x:x[0],trainingSet))

            with open(dMani.conf["path"]["stopwordList"]) as f:
                stopword=f.readlines()
            self.stopword=[x.strip() for x in stopword]
        
            for i in range(0,len(contents)):
                contents[i]=TFIDFSplitter.split(contents[i])
            self.corpusMani=CorpusData.CorpusDataManipulator(contents,self.codes,indicator)#build all corpus Manipulator

            self.lsi=LsiModel.LsiModel(self.corpusMani,indicator)#get LSI Model

    def voting(self,result):
        result = list(map(lambda x:[x[0],math.tan(x[1]*math.pi/2)],result))
        print(result)
        voted={}
        for i in result:
            if i[0] not in list(voted.keys()):
                voted[i[0]]=i[1]
            else:
                voted[i[0]]+=i[1]
        voted=sorted(list(voted.items()),key=lambda x:x[1],reverse=True)
        return voted
    def inquryDiagnosis(self,diagnosis,model=None,corpusMani=None):
        if model is None:
            model=self.lsi
        if corpusMani is None:
            corpusMani=self.corpusMani

        logging.info([x for x in TFIDFSplitter.split(diagnosis)])
        #DiagVec=corpusMani.doc2bow(list(filter(lambda x: x not in self.stopword,jiebaCutAll(diagnosis,False))))
        DiagVec=corpusMani.doc2bow(TFIDFSplitter.split(diagnosis))


        result = model.predict(DiagVec)# get a list of score and corresponding document
        result=list(map(lambda x: tuple([self.getCode(x[0]),x[1]]),result[:30]))
        result= self.voting(result)
        
        return result#list(map(lambda x: tuple([self.getCode(x[0]),x[1]]),result[:30])) #returns a list with some pair of DiagCode and its score(probability)
    
    def retrain(self):
        self.lsi.versionProcceed()
        self.lsi.reindex()
        
    def addDocuments(self,docs):
        logging.info("added docs:%s",(docs))
        self.lsi.addDocuments(docs)
        logging.info('code add!')
    
    def getCode(self,documentNo):
        return self.corpusMani.getCode(documentNo)
    def cutDiag(self,diag):
        return list(filter(lambda x: x not in self.stopword,jiebaCutAll(diag,False)))
    
class DiagInqury:
    def __init__(self):
        self.dispatcher={}
        self.inquryer=DiagInquryer()
        self.dispatcher['diagQuery']=lambda ins:list(map(lambda x:tuple([x[0],1.*x[1]]),self.inquryer.inquryDiagnosis(ins['diag'])))
        #self.dispatcher['retrain']=lambda ins:self.inquryer.retrain()
        self.dispatcher['addDocuments']=lambda ins: self.addDocs(ins)
        self.dispatcher['getSentenceCut']=lambda ins:self.inquryer.cutDiag(ins['sentence'])
        self.dispatcher['SaveProfiles']=lambda ins:self.SaveProfiles()
        
    def SaveProfiles(self):
        self.inquryer.corpusMani.saveCorpusAndCodes()
        self.inquryer.lsi.saveProfile()
        return 0

    def inqury(self,ins):
        logging.info(ins)
        #logging.info(self.dispatcher[ins['instruction']])
        return self.dispatcher[ins['instruction']](ins)

    def addDocs(self,ins):
        wordVecs=list(map(TFIDFSplitter.split,ins['docs']))
        #print([x for x in wordVecs])#get word Vector
        self.inquryer.corpusMani.addVecToDic(wordVecs)
        idVecs=[self.inquryer.corpusMani.doc2bow(x) for x in wordVecs]
        #print(idVecs)

        diagCodeDic=dict(map(tuple,(map(lambda x,y:[",".join(TFIDFSplitter.split(x)),y],ins['docs'],ins['code']))))
        diagnosesData.diagnosesManipulator.diagCodeDic.update(diagCodeDic)
        
        addedVec=self.inquryer.corpusMani.addVecToCorpus(idVecs,ins['code'])
        self.inquryer.addDocuments(addedVec)
        self.inquryer.retrain()