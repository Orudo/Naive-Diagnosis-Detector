import json
class dataManipulator:
    conf=json.loads(open("/home/martin/Naive-Diagnosis-Detector/data/Conf.json").read())
    trainingData=json.loads(open(conf["path"]["trainingData"]).read())
    diagnoses=list(map(lambda x:x[0],trainingData))
    codes=list(map(lambda x:x[1],trainingData))
    @staticmethod
    def extendDiagnoses(data):
        diagnoses.extend(map(lambda x:x[0],data))
        codes.extend(map(lambda x:x[1],data))
    @staticmethod
    def writeDiagsToDisk():
        with open(conf["path"]["trainingData"],"w") as f:
            f.write(json.dumps(list(map(lambda x,y:[x,y],diagnoses,codes))))
        
