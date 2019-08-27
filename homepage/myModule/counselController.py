from flask import request, jsonify, render_template
from datetime import datetime
from myModule import counselingdao
from settings import APP_STATIC
from keras import backend as K
from keras.models import load_model
import pandas as pd
import json
import os
from myModule.getSolutionController import getSolution


class CounselController():
    def __init__(self):
        pass


    def getBigcate(self):
        bigCate = counselingdao.getBigCate()
        return render_template('index.html', big_cate=bigCate)


    def updateMidcate(self):
        selected_class = request.args.get('selected_big', type=str)
        updated_values = counselingdao.getMidCate(selected_class)

        html_string_selected='<option value="">전체</option>';
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry['mname'], entry['mname'])

        return jsonify(html_string_selected=html_string_selected)


    def updateSmallcate(self, bigCate, midCate):
        updated_values = counselingdao.getSmallCate(bigCate, midCate)

        html_string_selected = '<option value="">전체</option>';
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry['sname'], entry['sname'])

        return jsonify(html_string_selected=html_string_selected)


    # 상담글 작성
    def writeCounsel(self):
        title = request.form.get('inputTitle')
        big = request.form.get('SelectBigCate')
        mid = request.form.get('SelectMidCate')
        small = request.form.get('SelectSmallCate')
        question_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        question = request.form.get('inputContent')

        # 답변을 여기다가 넣기

        counsel = {'title': title, 'big_cate': big, 'mid_cate': mid, 'small_cate': small,
                   'question_date': question_date,
                   'question': question}
        tags, gijun, cname = getSolution(counsel)
        print(tags)
        if gijun == -1:
            gijun = '고객님이 질문하신 내용에 대한 적당한 해결기준을 찾지 못하였습니다.'
        # counsel['tags'] = tags
        # counsel['answer'] = gijun
        counselingdao.setCounseling(counsel)
        result = counselingdao.getCounseling(question_date)
        print('gijun은 ', gijun)

        # counselingdao.setTagsresult[0]['id']

        # 들어온 상담에 대해서 결과값 출력
        # gijun = getSolution(counsel)

        return result, tags, gijun, cname


    # 모델을 통한 예측
    def predictModel(self):
        big = request.form.get('SelectBigCate')
        print(big)

        addPaperModel = load_model(os.path.join(APP_STATIC, 'predictModel/'+big+'_add_paper.h5'))
        addPaperModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        goojaeModel = load_model(os.path.join(APP_STATIC, 'predictModel/' + big + '_goojae.h5'))
        goojaeModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        jojungModel = load_model(os.path.join(APP_STATIC, 'predictModel/'+big+'_jojung.h5'))
        jojungModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        negoableModel = load_model(os.path.join(APP_STATIC, 'predictModel/'+big+'_nego_able.h5'))
        negoableModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


        with open(os.path.join(APP_STATIC, 'predictModel/tag_list.json')) as f:
            List = json.load(f)
        a = ['환불', '디조', '요금', 'as']
        tt = pd.DataFrame([[1 if _ in a else 0 for _ in List[big]]])

        print("추가서류 여부 예측")
        print(addPaperModel.predict(tt))
        print("구제 예측")
        print(goojaeModel.predict(tt))
        print("조정 예측")
        print(jojungModel.predict(tt))
        print("협상 예측")
        print(negoableModel.predict(tt))
        K.clear_session()


counselController = CounselController()
