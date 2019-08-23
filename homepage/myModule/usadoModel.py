from konlpy.tag import Kkma, Okt
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import time
from gensim.models import Word2Vec


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
                print(
                    f'제목 : {self.title[argsort[0][idx]]} index : {argsort[0][idx]} 유사도 : {(multiple[0][argsort[0][idx]] * 100).round(2)}%')
                index_list.append(argsort[0][idx])
                #                 similar_list.append(multiple[0][argsort[0][idx]])
                idx += 1
                n += 1

        return index_list, multiple

    def topIndex(self, input_text, top=5):
        index_list = []
        self.title.insert(0, input_text)
        self.okt_noun_add(input_text)
        index_list, mul = self.get_info(self.doc_list, top)

        self.doc_list.pop(0)
        self.title.pop(0)

        return list(map(lambda x: x - 1, index_list)), mul

    def getReceiptNum(self, input_text, top=5):
        index_list, mul = self.topIndex(input_text, top)
        return list(map(lambda x: self.data_recp_num[x], index_list))

    def weight_comp(self, input_1, weight=0.35, top=5):
        print(f'\n-------------------입력 단어기반 분석(weight={weight})---------------------\n')
        idx1, sim1 = self.topIndex(input_1, top)
        print(f'\n----------입력 단어기반 word2vce 적용한 분석(weight={1 - weight})----------------\n')
        idx2, sim2 = self.topIndex(self.getvector(input_1), top)
        print('\n---------------------------결과------------------------------------------\n')
        ssim = sim1 * weight + sim2 * (1 - weight)
        n = 0
        idx = 0
        sum_index_list = list()
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
                print(
                    f'제목 : {self.title[int(argsort[0][idx]) - 1]} index : {int(argsort[0][idx]) - 1} 유사도 : {(ssim[0][argsort[0][idx]] * 100).round(2)}%')
                sum_index_list.append(argsort[0][idx])
                #                 similar_list.append(multiple[0][argsort[0][idx]])
                idx += 1
                n += 1

    # 덧셈 후 cos 유사도 계산
    def getvector(self, text):
        v_f = np.zeros(shape=(self.model.wv.vectors.shape[1],))
        pr = list()
        text_list = text.split(' ')
        for line in text_list:
            v_f += self.model.wv.get_vector(line)
        sim = self.model.wv.cosine_similarities(v_f, self.model.wv.vectors)
        argsim = np.argsort(-sim)
        for idx in argsim[:10]:
            pr.append(self.model.wv.index2word[idx])
        chec = ' '.join(pr)
        print(chec)
        return chec
