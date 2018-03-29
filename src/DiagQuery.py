from NLPUtilities import *
import LsiModel
import CorpusData
import TFIDFSplitter
import logging
import jieba
import time
import dataManipulator
import diagnosesData
import json
import math
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
jieba.add_word(u'裂伤',3,'n')
jieba.add_word(u'头皮',3,'n')
jieba.add_word(u'软组织',3,'n')
jieba.add_word(u'挫裂伤',3,'n')



'''with open("/home/martin/NLPTest/data/DiagTrainingSet.Code") as f:
    codes=f.readlines()

codes=[x.strip() for x in codes]'''



class DiagInquryer:
    def confinit(self):
        jsonData=open("/home/martin/Naive-Diagnosis-Detector/data/Conf.json").read()
        conf=json.loads(jsonData)

        self.conf=conf

    def __init__(self):
        #self.confinit()
        dMani=dataManipulator.dataManipulator()
        #print()
        #jieba.load_userdict("/home/martin/NLPTest/data/jiebaDic")
        jieba.load_userdict(dMani.conf["path"]["jiebaDic"])
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        #with open("/home/martin/NLPTest/data/DiagTrainingSet.Code") as f:
        '''with open(self.conf["path"]["diagnosisTrainingSetCode"]) as f:
            codes=f.readlines()
        self.codes=[x.strip() for x in codes]'''

        trainingSet=json.loads(open(dMani.conf["path"]["trainingSet"]).read())
        self.codes=list(map(lambda x:x[1],trainingSet))
        contents=list(map(lambda x:x[0],trainingSet))



        #with open("/home/martin/NLPTest/data/stopword.list") as f:
        with open(dMani.conf["path"]["stopwordList"]) as f:
            stopword=f.readlines()
        self.stopword=[x.strip() for x in stopword]
       
        '''with open("/home/martin/NLPTest/data/trainingSet.data") as f:
            contents=f.readlines()
        contents=[x.strip() for x in contents]'''
        #contents=[TFIDFSplitter.split(i) for i in contents]
        for i in range(0,len(contents)):
            #print(contents[i])
            contents[i]=TFIDFSplitter.split(contents[i])
            #print(contents[i])
        self.corpusMani=CorpusData.CorpusDataManipulator(contents,self.codes)#build all corpus Manipulator

        self.lsi=LsiModel.LsiModel(self.corpusMani)#get LSI Model


        '''with open("/home/martin/NLPTest/data/stopword.list") as f:
            stopword=f.readlines()
        self.stopword=[x.strip() for x in stopword]'''
    def voting(self,result):
        result = list(map(lambda x:[x[0],math.tan(x[1]*math.pi/2)],result))
        print(result)
        voted={}
        for i in result:
            #print(i)
            #time.sleep(3000)
            #print(list(voted.keys()))
            if i[0] not in list(voted.keys()):
                voted[i[0]]=i[1]
            else:
                voted[i[0]]+=i[1]
        voted=sorted(list(voted.items()),key=lambda x:x[1],reverse=True)
        print(voted)
        #return list(voted.items())
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
        #self.codes.insert(len(self.codes),code)
        #self.codes.extend(codes)
        #self.codes.append(code)

    
    def getCode(self,documentNo):
        #return diagnosesData.diagnosesManipulator.diagCodeDic[",".join(self.corpusMani.bow2doc(self.corpusMani.getText(documentNo)))]
        return self.corpusMani.getCode(documentNo)
        #return documentNo
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
        
    def inqury(self,ins):
        logging.info(ins)
        #logging.info(self.dispatcher[ins['instruction']])
        return self.dispatcher[ins['instruction']](ins)
        '''if ins['instruction']=="diagQuery":
            logging.info(ins['diag'])
            return list(map(lambda x:tuple([x[0],1.*x[1]]),self.inquryer.inquryDiagnosis(ins['diag'])))'''
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

'''def main():
    

    

    with open("/home/martin/NLPTest/data/test.set") as f:
        tests=f.readlines()

    with open("/home/martin/NLPTest/data/stopword.list") as f:
        stopword=f.readlines()

    stopword=[x.strip() for x in stopword]
    #print(stopword)
    tests=[x.strip() for x in tests]
    #testset=[corpusMani.doc2bow(filter(lambda x: x not in stopword,jieba.cut(x,cut_all=True,HMM=False))) for x in tests]

    logging.critical("prediction is over")
    

    start = time.time()
    for i in tests:
        print(inquryDiagnosis(i,lsi,corpusMani))
        logging.critical("time cost:"+str(time.time()-start))
        start=time.time()

    #for i in lsi.batchPredict(testset):
        
        #print(list(map(lambda x: tuple([getCode(x[0]),x[1]]),i[:5])))

'''
'''if __name__=='__main__':
    main()
'''
