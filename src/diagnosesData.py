import dataManipulator
import TFIDFSplitter
import json

class diagnosesManipulator:
    diagnoses=list(map(lambda x:x[0],dataManipulator.dataManipulator.trainingData))
    codes=list(map(lambda x:x[1],dataManipulator.dataManipulator.trainingData))
    diagCodeDic=dict(map(tuple,(map(lambda x:[",".join(TFIDFSplitter.split(x[0])),x[1]],dataManipulator.dataManipulator.trainingData))))
    print(diagCodeDic)
    @staticmethod
    def extendDiagnoses(data):
        diagnoses.extend(map(lambda x:x[0],data))
        codes.extend(map(lambda x:x[1],data))
    @staticmethod
    def writeDiagsToDisk():
        with open(conf["path"]["trainingData"],"w") as f:
            f.write(json.dumps(list(map(lambda x,y:[x,y],diagnoses,codes))))