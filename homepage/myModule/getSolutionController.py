import requests
import json
import urllib3
import re
from collections import Counter
from settings import APP_STATIC
import os
from myModule.tagStudy import model
from myModule import counselingdao

with open(os.path.join(APP_STATIC, 'mobum_tagging_data.json')) as c:
    mobum_tagging_data = json.load(c)
with open(os.path.join(APP_STATIC, 'imp_data.json')) as c:
    situList = json.load(c)

def getMorph(text, type):
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
    dictData = eval(response.data)

    sen_dict = dict()
    sentence_noun_list = list()
    sentences = dictData['return_object']['sentence']

    morList = []
    for s in sentences:
        morp = s['morp']
        for _ in morp:
            if _['type'][0:3] == 'NNG' or _['type'][0:3] == 'NNP':
                if _['weight'] > 0.05:
                    morList.append(_['lemma'])
            if type == 1:
                if _['type'] == 'SL' or _['type'] == 'SN':
                    morList.append(_['lemma'])

    return morList

# 제목+내용을 가지고 형태소 데이터 만드는 함수
def makeMorphList(text):
    morph_list = []
    text_morph = getMorph(text, 1)  # 형태소 리스트
    morph_list.append(text_morph)  # 형태소 리스트 추가

    count = Counter(text_morph)
    keywords = []
    for w, c in count.most_common(15):
        if len(w) > 1:
            temp = {'tag': w, 'count': c}
            keywords.append(temp['tag'])
    morph_list.append(keywords)  # 키워드 형태소 리스트 추가

    return morph_list

def spellchecker(text):
    url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"
    params = {
        '_callback': 'mycallback',
        'q': text,
        'where': 'nexearch',
        'color_blindness': '0'
    }

    if len(text) > 500:
        return

    response = requests.get(url, params=params).text
    response = response.replace(params['_callback'] + '(', '').replace(');', '')
    response_dict = json.loads(response)
    result = response_dict['message']['result']['notag_html']
    result = re.sub(r'<\/?.*?>', '', result)

    return result

# 태그 생성 함수
def getTags(morph_list, mobums, mobumLength):
    mobumDict = dict()
    text_tag = []
    # 해당 중분류의 모범상담이 1개 이상이면
    if mobumLength != 0:
        for mobumIdx, mobum in enumerate(mobums):
            cnt = 0
            # 제목/내용 부분
            for morph in morph_list[0]:
                if morph in mobum:
                    cnt += 1
                else:
                    continue
            # 키워드 부분
            for morph in morph_list[1]:
                if morph in mobum:
                    cnt += 2
                else:
                    continue
            mobumDict[mobumIdx] = cnt
        sortedItem = sorted(mobumDict.items(), key=lambda k: k[1], reverse=True)
        tagNum = sortedItem[0][0]  # 가장 많은 빈도수를 가진 모범사례 추출

        for morph in morph_list[0]:
            if morph in mobums[tagNum] and morph not in text_tag:
                text_tag.append(morph)

            if morph in situList and morph not in text_tag:
                text_tag.append(morph)
    # 모범상담이 존재하지 않으면
    else:
        for morph in morph_list[0]:
            if morph in situList and morph not in text_tag:
                text_tag.append(morph)

    return text_tag


# 태그와 유사한 단어 묶음의 태그 생성
def getSimilarTags(text_tag, type):
    similar_tag = []
    exist = []
    for tag in text_tag:
        similar_tag.append(tag)
        exist.append(tag)

        try:
            if type == 1:
                tmp = model.wv.most_similar(tag)[0:3]
            else:
                tmp = model.wv.most_similar(tag)[0:2]

            for _ in tmp:
                if _[0] not in exist:
                    similar_tag.append(_[0])

        except KeyError:
            continue

    return similar_tag


# 해당 해결기준과 각각의 빈도수 추출
# item = 소분류, itemCode = 중분류
def cmpGijun(similar_tag, item, itemcode):
    chk = counselingdao.countGijunBySmall(item)

    if chk==():
        chk2 = counselingdao.countGijunByMiddle(itemcode)
        if chk2 == ():
            print('해당 해결기준이 존재하지 않습니다.')

    typedict = dict()

    # 결과값이 있을때
    if chk != () or chk2 != ():
        if chk == ():
            res = chk2
        else:
            res = chk
        cid = res[0]['category_id']
        cname = res[0]['category_name']

        for type in res:
            cnt = 0
            type_tag = getMorph(spellchecker(type['type_1']), 2)
            similar_type_tag = getSimilarTags(type_tag, 2)

            for _ in similar_tag:
                if _ in similar_type_tag:
                    cnt += 1
            typedict[type['type_1']] = cnt

        return typedict, cid, cname
    else:
        return typedict, -1, None


# 선택된 해결기준 상세내용 불러오기
def getGijun(sortdict, id):
    max = -1
    max2 = 0
    maxlist = []
    gijunlist = []
    print(sortdict, id)
    for _ in sortdict:
        if max < _[1]:
            max = _[1]

    for idx,_ in enumerate(sortdict):
        if _[1] == max:
            maxlist.append(_[0])
        elif _[1] != max and _[1] != 0 and idx == 1:
            max2 = _[1]
            maxlist.append(_[0])
        elif _[1] == max2 and idx == 2:
            del(maxlist[-1])

    # 빈도수 1순위가 3개 이내일 때만 출력
    if len(maxlist) < 4:
        for _ in maxlist:
            gijunlist.append(counselingdao.getGijunList(_, id))
    else:
        print('해당 해결기준이 존재하지 않습니다.')

    print('final 기준리스트 ', gijunlist)
    return gijunlist


# 해결기준 뿌려주기
def showGijun(gijunlist):
    type1, type2, type3, bigo = [], [], [], []
    ans = ''
    for i, gijun in enumerate(gijunlist):
        for i2, _ in enumerate(gijun):
            # type2가 없으면 type1, std 출력
            if _['type_2'] == '':
                ans += _['type_1'] + ' → ' + _['standard'] + '|'
                type1.append(_['type_1'])

            # type2가 있으면
            else:
                if _['type_1'] not in type1:
                    type1.append(_['type_1'])
                    ans += _['type_1'] + '|'

                # type3이 없으면 type2, std 출력
                if _['type_3'] == '':
                    ans += '@- ' + _['type_2'] + ' → ' + _['standard'] + '|'
                    type2.append(_['type_2'])

                # type3가 있으면
                else:
                    if _['type_2'] not in type2:
                        type2.append(_['type_2'])
                        ans += '@- ' + _['type_2'] + '|'

                    # type4가 없으면 type3, std 출력
                    if _['type_4'] == '':
                        ans += '#- ' + _['type_3'] + ' → ' + _['standard'] + '|'
                        type3.append(_['type_3'])

                    # type4가 있으면
                    else:
                        if _['type_3'] not in type3:
                            type3.append(_['type_3'])
                            ans += '#- ' + _['type_3'] + '|'

                        ans += '$- ' + _['type_4'] + ' → ' + _['standard'] + '|'

            # 비고 출력
            if _['bigo'] != '':
                if _['bigo'] not in bigo:
                    bigo.append(_['bigo'])

                    if len(bigo) >= 2:
                        ans += '|' + '비고 : ' + bigo[-2] + '|'

                if i == len(gijunlist) - 1 and i2 == len(gijun) - 1:
                    ans += '|' + '비고 : ' + bigo[-1]

            if i2 == len(gijun) - 1:
                ans += '|'

    return ans


# 실행함수
def getSolution(ques):
    itemcode = ques['mid_cate']
    item = ques['small_cate']
    q = ques['question']
    # question 부분 앞의 양식 제거하기 위함
    if q[0:8] == '문의 내용은 [':
        newQuestion = q.replace(q[:217], '')
    else:
        newQuestion = q
    text = spellchecker(ques['title']) + ' ' + newQuestion

    # 태깅을 위한 해당 중분류 모범상담 태그 데이터 불러오기
    mid_id = counselingdao.getMobum(itemcode)
    mobums = mobum_tagging_data[mid_id[0]['id'] - 1]
    mobumLength = len(mobums)

    # 형태소 생성
    morph_list = makeMorphList(text)

    # 태깅 시작
    text_tag = getTags(morph_list, mobums, mobumLength)

    # 해결기준과의 매칭을 위한 태깅 데이터의 유사단어 갖고오기
    similar_tag = getSimilarTags(text_tag, 1)

    # 관련 해결기준 불러오기
    typedict, cid, cname = cmpGijun(similar_tag, item, itemcode)
    if cid != -1:
        sortdict = sorted(typedict.items(), key=lambda k: k[1], reverse=True)

        # 선택된 해결기준 내용 불러오기
        gijunlist = getGijun(sortdict, cid)
        print('getSolution gijunList', gijunlist)
        if gijunlist != []:
            # 내용 뿌려주기
            solution = showGijun(gijunlist)
        else:
            return text_tag, -1, None
    else:
        return text_tag, -1, None

    return text_tag, solution, cname