import functools
import json


class dataManipulator:
    conf=json.loads(open("/home/martin/Naive-Diagnosis-Detector/data/Conf.json").read())
    trainingData=json.loads(open(conf["path"]["trainingSet"]).read())
    