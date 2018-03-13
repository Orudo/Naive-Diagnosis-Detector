from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.naive_bayes import MultinomialNB
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train',categories=categories, shuffle=True)

print(twenty_train.target_names)
print(len(twenty_train.data))
print(print("\n".join(twenty_train.data[0].split("\n")[:3])))
print(twenty_train.target[:10])

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
print(X_train_counts[0])

tf_transformer = TfidfTransformer(use_idf=True).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
print(X_train_tf.tolist())


clf = MultinomialNB().fit(X_train_tf, twenty_train.target)
#clf= KMeans(n_clusters=4).fit(X_train_tf)
print(clf.predict(X_train_tf)[:10])

docs_new = ['God is love', 'OpenGL on the GPU is fast','Hello World']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tf_transformer.transform(X_new_counts)

logging.info("K-NN model training is over!")
print(clf.predict(X_new_tfidf) )
#predicted = clf.predict(X_new_tfidf)
'''for i in range(0,len(X_new_counts)):
    predicted = clf.index(i)
    print(predicted)'''

'''for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
'''