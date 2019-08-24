from konlpy.tag import Kkma, Okt
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import time
from gensim.models import Word2Vec
import pickle
import requests
import urllib3

doc = pickle.load(open('./static/sum_doc.pkl', 'rb'))
data = pickle.load(open('./static/sum_data.pkl', 'rb'))
result = pickle.load(open('./static/sum_result.pkl', 'rb'))
title = pickle.load(open('./static/sum_title.pkl', 'rb'))

class test_model():
    def __init__(self, title, doc, data_num, result):
        self.data_recp_num = data_num
        self.title = title
        self.doc_list = doc
        self.model = Word2Vec(result, size=300, window=5, min_count=5, workers=4)
        self.model.init_sims()

    # 입력받은 title noun뽑아서 맨 앞에 insert
    def okt_noun_add(self, input_text):
        okt = Okt()
        doc = ''
        doc = ' '.join(okt.nouns(input_text))
        self.doc_list.insert(0, doc)

    def get_info(self, doc_list, top=5):

        tfidf_vectorizer = TfidfVectorizer(min_df=1)
        tfidf_matrix = tfidf_vectorizer.fit_transform(doc_list)

        multiple = tfidf_matrix[0, :] * tfidf_matrix.T

        multiple = multiple.toarray()

        argsort = np.argsort(-multiple)  # tfidf vectorize 계산한 multiple을 argsort를 이용해 높은순으로 정렬
        idx = 0
        n = 0
        index_list = list()
        similar_list = list()
        #     top5idx = argsort[0][:5] # 높은순으로 5개 뽑음
        print(f'검색할 제목 : {self.title[0]}')  # 검사할 상담 제목 출력
        while True:
            # 인덱스가 자기 자신이거나 유사도가 1일경우 제외
            if argsort[0][idx] == 0:
                idx += 1
                continue
            elif multiple[0][argsort[0][idx]] < 0.3:
                print('유사도가 30%이하로 너무 낮아 더이상 뽑을 수 없습니다')
                break
            elif n == top:
                break
            else:
                print(f'제목 : {self.title[argsort[0][idx]]} index : {argsort[0][idx]} 유사도 : {(multiple[0][argsort[0][idx]] * 100).round(2)}%')
                index_list.append(argsort[0][idx])
                #                 similar_list.append(multiple[0][argsort[0][idx]])
                idx += 1
                n += 1

        return index_list, multiple

    # 덧셈 후 cos 유사도 계산
    def getvector(self, text):
        v_f = np.zeros(shape=(self.model.wv.vectors.shape[1],))
        pr = list()
        print(text)
        text_1 = self.get_feature(text)
        print(text_1)
        text_list = text_1[0][0].split(' ')
        text_list2 = list()
        for noun in text_list:
            if noun in self.model.wv.vocab.keys():
                text_list2.append(noun)
            else:
                pass

        for line in text_list2:
            v_f += self.model.wv.get_vector(line)
        sim = self.model.wv.cosine_similarities(v_f, self.model.wv.vectors)
        argsim = np.argsort(-sim)
        for idx in argsim[:5]:
            text_list2.append(self.model.wv.index2word[idx])
        chec = ' '.join(text_list2)
        print(chec)
        return chec

    def topIndex(self, input_text, top=5):
        index_list = []
        self.title.insert(0, input_text)
        self.okt_noun_add(input_text)
        index_list, mul = self.get_info(self.doc_list, top)

        self.doc_list.pop(0)
        self.title.pop(0)

        return list(map(lambda x: x - 1, index_list)), mul

    # 단어 기반 비교 후 접수번호 가져오는 함수
    def get_receipt_num(self, input_text, top=5):
        index_list, mul = self.topIndex(input_text, top)
        return list(map(lambda x: self.data_recp_num[x], index_list))

    # word2vec 기반 비교 후 접수번호 가져오는 함수
    def get_word2vec_receipt_num(self, input_text, top=5):
        index_list, mul = self.topIndex(self.getvector(input_text), top)
        return list(map(lambda x: self.data_recp_num[x], index_list))

        # 두 방법의 유사도 분석 기법을 비교 후 알맞은 weight 보기위한 함수

    def weight_comp(self, input_1, weight=0.35, top=5):
        print(f'\n-------------------입력 단어기반 제목 비교 분석(weight={weight})---------------------\n')
        idx1, sim1 = self.topIndex(input_1, top)
        print(f'\n----------입력 단어기반 word2vce 적용한 태깅 분석(weight={1 - weight})----------------\n')
        idx2, sim2 = self.topIndex(self.getvector(input_1), top)
        print('\n---------------------------결과------------------------------------------\n')
        ssim = sim1 * weight + sim2 * (1 - weight)
        n = 0
        idx = 0
        sum_index_list = list()
        sum_title_list = list()
        sum_similar_list = list()
        argsort = np.argsort(-ssim)
        while True:
            # 인덱스가 자기 자신이거나 유사도가 1일경우 제외
            if argsort[0][idx] == 0:
                idx += 1
                continue
            #             elif ssim[0][argsort[0][idx]] < 0.3:
            #                 print('유사도가 30%이하로 너무 낮아 더이상 뽑을 수 없습니다')
            #                 break
            elif n == top:
                break
            else:
                print(f'제목 : {self.title[int(argsort[0][idx]) - 1]} index : {int(argsort[0][idx]) - 1} 유사도 : {(ssim[0][argsort[0][idx]] * 100).round(2)} % ')
            sum_index_list.append(argsort[0][idx])
            sum_title_list.append(self.title[int(argsort[0][idx]) - 1])
            sum_similar_list.append((ssim[0][argsort[0][idx]] * 100).round(2))
            idx += 1
            n += 1

        return list(map(lambda x: self.data_recp_num[x], list(map(lambda x: x - 1, sum_index_list)))), sum_title_list, sum_similar_list

    # 분석을 위해 str 형식으로 변환
    def list2str(self, nounList):
        nounStr = ''
        for _ in nounList:
            nounStr += _ + ' '

        return nounStr

        # etri 형태소 분석 api를 이용하여 각 문장당 명사 형태소 추출하기

    def get_feature(self, text):
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
        accessKey = "0d25249a-3735-4736-9205-06bbb44a9084"
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

        text_length = len(sentences)

        for s in sentences:
            morp = s['morp']
            morp_list = list()

            for m in morp:
                # print(s['text'], m['lemma'])
                if m['type'][0:2] == 'NN' or m['type'] == 'VV':
                    morp_list.append(m['lemma'])

            morp_str = self.list2str(morp_list)
            sen_dict[s['text']] = morp_str

        for _ in sen_dict.values():
            sentence_noun_list.append(_)

        return sentence_noun_list, text_length, list(sen_dict.keys())

mobum_model=test_model(title, doc, data, result)

