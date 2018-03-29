import json
import urllib.request

with open("/mnt/d/BashOnWindowsExchange/Naive-Diagnosis-Detector/data/trainingSet.json") as f:
    tests=f.readline()

#tests=[x.strip() for x in tests]
validationData=json.loads(tests)
#print(validationData)


cnt=0
cnt_all=0
for i in validationData:
    conditionsSetURL = 'http://127.0.0.1:8080'
    newConditions = {'instruction':"diagQuery",'diag':i[0]} 
    #newConditions = {'instruction':"addDocument",'doc':"额骨多发骨折",'code':'S02.001'} 
    params = json.dumps(newConditions).encode('utf8')
    req = urllib.request.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    plainRes=response.read().decode('utf8')
    data=json.loads(plainRes)
    if data[0][1]>=100000000:
        if data[0][0]==i[1]:
            cnt+=1
        else:
            print(plainRes)
            print(i[1])
            print(i[0])
        cnt_all+=1

print(cnt/cnt_all)
        
'''conditionsSetURL = 'http://127.0.0.1:8080'
#newConditions = {'instruction':"diagQuery",'diag':"外眦至颞部、左耳屏、左颞皮肤挫裂伤"} 
newConditions = {'instruction':"addDocuments",'docs':["右上唇裂伤"],'code':['S01.500']} 
params = json.dumps(newConditions).encode('utf8')
req = urllib.request.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))
conditionsSetURL = 'http://127.0.0.1:8080'
newConditions = {'instruction':"diagQuery",'diag':"右上唇裂伤"} 
#newConditions = {'instruction':"addDocument",'doc':"额骨多发骨折",'code':'S02.001'} 
params = json.dumps(newConditions).encode('utf8')
req = urllib.request.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))'''
'''conditionsSetURL = 'http://127.0.0.1:8080'
#newConditions = {'instruction':"diagQuery",'diag':"外眦至颞部、左耳屏、左颞皮肤挫裂伤"} 
newConditions = {'instruction':"retrain"} 
params = json.dumps(newConditions).encode('utf8')
req = urllib.request.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))
'''
'''conditionsSetURL = 'http://127.0.0.1:8080'
newConditions = {'instruction':"diagQuery",'diag':"左枕部、左侧额颞顶部头皮挫裂伤"} 
#newConditions = {'instruction':"addDocument",'doc':"额骨多发骨折",'code':'S02.001'} 
params = json.dumps(newConditions).encode('utf8')
req = urllib.request.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))'''
