import json
import urllib.request

'''with open("/home/martin/Naive-Diagnosis-Detector/testdata.data") as f:
    tests=f.readlines()

tests=[x.strip() for x in tests]'''


'''for i in tests:
    conditionsSetURL = 'http://127.0.0.1:8080'
    newConditions = {'instruction':"diagQuery",'diag':i} 
    #newConditions = {'instruction':"addDocument",'doc':"额骨多发骨折",'code':'S02.001'} 
    params = json.dumps(newConditions).encode('utf8')
    req = urllib.request.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf8'))'''

conditionsSetURL = 'http://127.0.0.1:8080'
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
print(response.read().decode('utf8'))
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
