from konlpy.tag import Okt
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import time
import pickle
import requests
import urllib3

doc = pickle.load(open('./static/sum_doc.pkl', 'rb'))
data = pickle.load(open('./static/sum_data.pkl', 'rb'))
result = pickle.load(open('./static/sum_result.pkl', 'rb'))
title = pickle.load(open('./static/sum_title.pkl', 'rb'))

# with open(os.path.join(APP_STATIC, ("doc2vec.pkl", "rb"))) as file:
#     pkl_model_load = pickle.load(file)

pkl_model_load = pickle.load(open('./static/doc2vec.pkl', 'rb'))


class word2hybrid():
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

        while True:
            if argsort[0][idx] == 0:
                idx += 1
                continue
            elif multiple[0][argsort[0][idx]] < 0.3:
                break
            elif n == top:
                break
            else:
                index_list.append(argsort[0][idx])
                idx += 1
                n += 1

        return index_list, multiple

    # 덧셈 후 cos 유사도 계산
    def getvector(self, text):
        v_f = np.zeros(shape=(self.model.wv.vectors.shape[1],))
        text_1 = self.get_feature(text)
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
        n = 0
        for idx in argsim:
            if n == 5:
                break
            elif self.model.wv.index2word[idx] in text_list2:
                pass
            else:
                text_list2.append(self.model.wv.index2word[idx])
                n += 1
        chec = ' '.join(text_list2)
        return chec

    def topIndex(self, input_text, top=5):
        index_list = []
        self.title.insert(0, input_text)
        self.okt_noun_add(input_text)
        index_list, mul = self.get_info(self.doc_list, top)
        self.doc_list.pop(0)
        self.title.pop(0)

        return list(map(lambda x: x - 1, index_list)), mul

    def top_word2vec_index(self, input_text, top=5):
        index_list = []
        self.title.insert(0, input_text)
        self.doc_list.insert(0, input_text)
        index_list, mul = self.get_info(self.doc_list, top)
        self.doc_list.pop(0)
        self.title.pop(0)

        return list(map(lambda x: x - 1, index_list)), mul

    # 두 방법의 유사도 분석 기법을 비교 후 알맞은 weight 보기위한 함수
    def weight_comp(self, input_1, weight=0.35, top=5):
        idx1, sim1 = self.topIndex(input_1, top)
        idx2, sim2 = self.top_word2vec_index(self.getvector(input_1), top)
        ssim = sim1 * weight + sim2 * (1 - weight)
        result1 = self.get_list(sim1, top=top)
        result2 = self.get_list(sim2, top=top)
        result3 = self.get_list(ssim, top=top)
        return result1, result2, result3

    # 유사도 매트릭스를 가지고 title과 접수번호와 유사도 리스트를 가지고 있는 리스트셋 리턴 시켜주는 함수
    def get_list(self, similarity, top=5):
        n = 0
        idx = 0
        result_result = list()
        sum_index_list = list()
        sum_title_list = list()
        sum_similar_list = list()
        argsort = np.argsort(-similarity)
        while True:
            if argsort[0][idx] == 0:
                idx += 1
                continue
            elif similarity[0][argsort[0][idx]] < 0.35:
                #                 print('유사도가 35%이하로 너무 낮아 더이상 뽑을 수 없습니다')
                break
            elif n == top:
                break
            else:
                #                 print(f'제목 : {self.title[int(argsort[0][idx])-1]} index : { int(argsort[0][idx])-1 } 유사도 : {(ssim[0][argsort[0][idx]]*100).round(2)}%')
                sum_index_list.append(argsort[0][idx])

                if len(self.title[int(argsort[0][idx]) - 1]) > 24:
                    sum_title_list.append(self.title[int(argsort[0][idx]) - 1][:21] + '…')
                else:
                    sum_title_list.append(self.title[int(argsort[0][idx]) - 1])

                if similarity[0][argsort[0][idx]] > 1:
                    sum_similar_list.append(round(100, 2))
                else:
                    sum_similar_list.append((similarity[0][argsort[0][idx]] * 100).round(2))

                sum_recp_list = list(
                    map(lambda x: self.data_recp_num[x], list(map(lambda x: x - 1, sum_index_list))))
                idx += 1
                n += 1
        result_result.append(sum_recp_list)
        result_result.append(sum_title_list)
        result_result.append(sum_similar_list)
        return result_result

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
                if m['type'][0:2] == 'NN' or m['type'] == 'VV':
                    morp_list.append(m['lemma'])

            morp_str = self.list2str(morp_list)
            sen_dict[s['text']] = morp_str

        for _ in sen_dict.values():
            sentence_noun_list.append(_)

        return sentence_noun_list, text_length, list(sen_dict.keys())


class word2hybrid_update(word2hybrid):
    def __init__(self, title, doc, data_num, result, pkl_model):
        super().__init__(title, doc, data_num, result)
        self.doc2vec_model = pkl_model
        self.documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(result)]

    def text_pre_processing(self, input_text):
        text_feature = super().get_feature(input_text)
        text_list = text_feature[0][0].split(' ')
        final_text_list = list()
        for noun in text_list:
            if noun in self.model.wv.vocab.keys():
                final_text_list.append(noun)
            else:
                pass

        return final_text_list

    def text2doc(self, text_list):
        doc = TaggedDocument(text_list, [0])
        return doc.words

    def text2sims(self, input_text):
        text_list = self.text_pre_processing(input_text)
        doc = self.text2doc(text_list)
        ranks = []
        second_ranks = []
        inferred_vector = self.doc2vec_model.infer_vector(doc)
        sims = self.doc2vec_model.docvecs.most_similar([inferred_vector], topn=10)
        title_list = []
        recp_num_list = []
        idx_list = []
        sims_list = list(map(lambda x: round(x[1] * 100, 2), sims))

        for idx, sim in sims:
            title_list.append(self.title[idx])
            recp_num_list.append(self.data_recp_num[idx])
            idx_list.append(idx)

        return recp_num_list, title_list, sims_list, idx_list

    def weight_comp(self, input_1, update=[], update_weight=1.1, weight=0.35, top=5):
        idx1, sim1 = self.topIndex(input_1, top)
        idx2, sim2 = self.top_word2vec_index(self.getvector(input_1), top)
        ssim = sim1 * weight + sim2 * (1 - weight)
        for idx in update:
            ssim[0][idx + 1] = ssim[0][idx + 1] * update_weight

        result1 = self.get_list(sim1, top=top)
        result2 = self.get_list(sim2, top=top)
        result3 = self.get_list(ssim, top=top)
        return result1, result2, result3

    def doc2vec_weight_comp(self, input_text, update_weight=1.1, weight=0.35, top=5):
        sims_list = self.text2sims(input_text)
        return self.weight_comp(input_text, update=sims_list[3], update_weight=update_weight, weight=weight, top=top)


doc2vec_model = word2hybrid_update(title, doc, data, result, pkl_model_load)
