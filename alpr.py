import requests
import json
def getresult(picpath):
    with open(picpath, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp),
            headers={'Authorization': 'Token 27e09021020999e03b737a72dbbe99f68e8c840e'})    #change token here
    res=response.json()
    temp=res['results']
    try:
        finalResult=temp[0]['plate']
    except IndexError:
        print("Number plate not found!")
        return -1
    return finalResult
