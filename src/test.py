from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.models import LsiModel
import logging
import time
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = LsiModel(common_corpus[:3], id2word=common_dictionary)  # train model
vector = model[common_corpus[4]]  # apply model to BoW document
model.add_documents(common_corpus[4:])  # update model with new documents

model.save(tmp_fname)  # save model
loaded_model = LsiModel.load(tmp_fname)  # load model
time.sleep(10)