import dataManipulator
import TFIDFSplitter
import json
import logging

class diagnosesManipulator:
    diagnoses=list(map(lambda x:x[0],dataManipulator.dataManipulator.trainingData))
    codes=list(map(lambda x:x[1],dataManipulator.dataManipulator.trainingData))

    
    @staticmethod
    def extendDiagnoses(data):
        diagnosesManipulator.diagnoses.extend(data[0])
        diagnosesManipulator.codes.extend(data[1])
    @staticmethod
    def writeDiagsToDisk():
        with open(dataManipulator.dataManipulator.conf["path"]["trainingSet"],"w") as f:
            f.write(json.dumps(list(map(lambda x,y:[x,y],diagnosesManipulator.diagnoses,diagnosesManipulator.codes))))
        logging.info("local diagnoses DB has been updated")