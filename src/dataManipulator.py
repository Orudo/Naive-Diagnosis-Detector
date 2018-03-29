import functools
import json


class dataManipulator:
    conf=json.loads(open("/mnt/d/BashOnWindowsExchange/Naive-Diagnosis-Detector/data/Conf.json").read())
    trainingData=json.loads(open(conf["path"]["trainingSet"]).read())
    