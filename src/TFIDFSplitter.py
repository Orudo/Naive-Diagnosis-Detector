import jieba.analyse
import dataManipulator

with open(dataManipulator.dataManipulator.conf["path"]["stopwordList"]) as f:
    stopword=f.readlines()
stopword=[x.strip() for x in stopword]


def split(sentence):
    ret=list(jieba.analyse.extract_tags(sentence,topK=10,withWeight=False))
    for i in list(filter(lambda x: x not in stopword,jieba.cut(sentence,False))):
        ret.append(i)
    
    return list(set(ret))#list(jieba.analyse.extract_tags(sentence,topK=10,withWeight=False)).extend(list(filter(lambda x: x not in stopword,jieba.cut(sentence,False))))
