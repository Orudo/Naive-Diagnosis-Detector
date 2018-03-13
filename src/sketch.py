from gensim import corpora, models, similarities
import gensim
import TFIDFSplitter
import jieba
import logging
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from sklearn.cluster import KMeans


jieba.load_userdict("/home/martin/NLPTest/data/jiebaDic")
def codeTransform(code):
    if code=='A' or code=='B' or code=='C' or code=='D' or code=='E' or code=='F' :
        return 'Group1'
    if code=='G' or code=='H' or code=='I' or code=='J':
        return 'Group1'
    if code=='K' or code=='L' or code=='M' or code=='N' :
        return 'Group1'
    if code=='O' or code=='P' or code=='Q':
        return 'Group1'
    if code=='R' or code=='S' or code=='T' or code=='U' or code=='Z' :
        return 'Group5'
    return 'Unknown'
def pad_or_truncate(some_list, target_len):
    return some_list[:target_len] + [0]*(target_len - len(some_list))

def numbering(mytuple):
    '''x=mytuple[0]
    y=mytuple[1]
    return int(x+(x+y-1)*(x+y)/2)'''
    return mytuple[0]

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

jieba.add_word(u'裂伤',3,'n')

with open("/home/martin/NLPTest/data/trainingSet.data") as f:
    contents=f.readlines()

contents=[x.strip() for x in contents]
cnt=0
for i in contents:
    cnt+=1
print(cnt)

with open("/home/martin/NLPTest/data/DiagTrainingSet.Code") as f:
    codes=f.readlines()

codes=[x.strip() for x in codes]
#codes=list(map(codeTransform,map(lambda x:x[0],codes)))
#print(contents)
#stopWord = frozenset(('上'，'下'，'左'，'右'))
contents=[TFIDFSplitter.split(x) for x in contents]
#contents=list((list,contents))
#print(contents)
#print(contents)
#contents=[[y for y in jieba.cut(x,cut_all=True)] for x in contents]


dictionary = corpora.Dictionary(contents)
dictionary.save('/home/martin/NLPTest/data/deerwester.dict')

#print(dictionary.token2id)
with open("/home/martin/NLPTest/data/test.set") as f:
    tests=f.readlines()

with open("/home/martin/NLPTest/data/stopword.list") as f:
    stopword=f.readlines()

stopword=[x.strip() for x in stopword]
#print(stopword)
tests=[x.strip() for x in tests]
for i in tests:
    print(list(filter(lambda x: x not in stopword,jieba.cut(i,cut_all=True,HMM=False))))
#testset=[dictionary.doc2bow(filter(lambda x: x not in stopword,jieba.cut(x,cut_all=True,HMM=False))) for x in tests]
#testset_1=list([list(map(numbering,x)) for x in testset])
#testset_1=np.array(list(map(lambda x:pad_or_truncate(x,10),testset_1)))
#print(dictionary.doc2bow(contents[0]))
corpus = [dictionary.doc2bow(x) for x in contents]
#corpus_1 = list([list(map(numbering,x)) for x in corpus])
#corpus_1=np.array(list(map(lambda x:pad_or_truncate(x,10),corpus_1)))

'''print(corpus_1)
print(testset_1)
print(np.array(codes))

clf = MultinomialNB().fit(np.array(corpus_1),np.array(codes))
logging.info("clf training is over!")
for x in clf.predict(testset_1):
    print(x)'''
#print([clf.predict(x) for x in testset_1])


tests=[x.strip() for x in tests]
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=256)
corpusLsi=lsi[corpus]
lsi.add_documents(corpus)

'''

corpusLsi=[list(map(lambda y:y[1],x)) for x in corpusLsi]
corpusLsi=list(map(lambda x:pad_or_truncate(x,257),corpusLsi))
corpusLsi=list(map(np.array,corpusLsi))
#print(corpusLsi)
#print(np.array([x for x in corpusLsi[:50]]))
CorpusLsi=np.array(corpusLsi)
print(CorpusLsi)

testset=lsi[testset]
print(testset)
testset=[list(map(lambda y:y[1],x)) for x in testset]
testset=list(map(lambda x:pad_or_truncate(x,257),testset))
testset=list(map(np.array,testset))
testset=np.array(testset)

    

clf= KMeans(n_clusters=6).fit(CorpusLsi)
for x in testset:
    print(clf.predict(x.reshape(1,-1)))
index = similarities.MatrixSimilarity(lsi[corpus])
print(len(dictionary.items()))
print(lsi.id2word)
for new_doc in tests:
    print (new_doc)
    #print (", ".join(jieba.cut_for_search(new_doc)))
    #new_vec=dictionary.doc2bow(jieba.cut(new_doc,cut_all=True))
    new_vec=dictionary.doc2bow(filter(lambda x: x not in stopword,jieba.cut(new_doc,cut_all=True,HMM=False)))
    print(", ".join(filter(lambda x: x not in stopword,jieba.cut(new_doc,cut_all=True))))
    #new_vec=dictionary.doc2bow(TFIDFSplitter.split(new_doc))
    #new_vec=filter(lambda x: x not in stopword,new_vec)
    #new_vec=[x for x in new_vec]
    #print([x for x in new_vec])
    
    #print(corpus)



    vec_lsi=lsi[new_vec]

    
    print(lsi[corpus])

    sims = index[vec_lsi]

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    #print(sims)

    print(codes[(sims[0])[0]]+str(sims[0])+str(sims[1])+str(sims[2]))
    
print(dictionary.num_pos)'''
