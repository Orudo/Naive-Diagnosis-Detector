from gensim import corpora, models, similarities


class lsiClassificationModel:
    def __init__(self,corpus,dictionary,num_topics=128):
        self.lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
        self.index = similarities.MatrixSimilarity(lsi[corpus])
    
    def classify(self,vec)
        return sims=index[lsi[vec]]

    def retrain(self,corpus,dictionary,num_topics=128):
        self.lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
        self.index = similarities.MatrixSimilarity(lsi[corpus])
