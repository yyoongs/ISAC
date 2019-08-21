import requests
import json
import urllib3

def getMorph(text):
    print('h1')
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "bf0500d9-cbdf-4a99-b84f-1020c9f829cd"
    analysisCode = "morp"
    text = text

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    data = str(response.data, "utf-8")
    dictData = eval(data)

    sen_dict = dict()
    sentence_noun_list = list()
    sentences = dictData['return_object']['sentence']

    morList = []
    for s in sentences:
        # print(s)
        morp = s['morp']
        for _ in morp:
            if _['type'][0:3] == 'NNG' or _['type'][0:3] == 'NNP':
                if _['weight'] > 0.05:
                    morList.append(_['lemma'])

    return morList