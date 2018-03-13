import jieba
import jieba.analyse
import gensim

#stopWordPATH=""

def jiebaCutAll(setence,HMM):#with inputing a sentence, this function returns a iteratable obj of separated word
    DiagVec_word = jieba.cut(setence,cut_all=True,HMM=HMM)
    return DiagVec_word#filter(lambda x: x not in stopWord,DiagVec_word)

def wordVec2idVec(WordVec,dictionary):
    return dictionary.doc2bow(WordVec)


'''class lsiContainer:
    def __init__(self,vecs,classficationResults,dictionary):
        self.LsiModels={}
        for i in range(0,len(classficationResult)):
            if classficationResult[i] in LsiModels:
                LsiModels[classficationResults[i]].add_documents([vecs[i]])
            if classficationResult[i] not in LsiModels:
                LsiModels[classficationResults[i]]=models.LsiModel([vec[i]], id2word=dictionary, num_topics=256)
    def similarityIndexing(self):
        for x in self.LsiModels:
            
    def getSimilarCode(self,vec,classficationResult):
        vecLsi=lsi[vec]'''


