import jieba
import dataManipulator
import logging
dMani=dataManipulator.dataManipulator
jieba.load_userdict(dMani.conf["path"]["jiebaDic"])
logging.basicConfig(filename=dataManipulator.dataManipulator.conf["path"]["logs"],format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
