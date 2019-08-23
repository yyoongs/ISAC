from flask import request, jsonify, render_template
from datetime import datetime
from myModule import counselingdao
from myModule.morpy import getMorph
from myModule import usadoModel as md
from settings import APP_STATIC
from keras.models import load_model
import pandas as pd
import pickle
import json
import os


doc_list = pickle.load(open('./static/sum_doc.pkl', 'rb'))
data_recp_num = pickle.load(open('./static/sum_data.pkl', 'rb'))
result2 = pickle.load(open('./static/sum_result.pkl', 'rb'))
title = pickle.load(open('./static/sum_title.pkl', 'rb'))

class CounselController():
    def __init__(self):
        pass


    def getBigcate(self):
        bigCate = counselingdao.getBigCate()
        return render_template('index.html', big_cate=bigCate)


    def updateMidcate(self):
        selected_class = request.args.get('selected_class', type=str)
        updated_values = counselingdao.getMidCate(selected_class)

        html_string_selected='<option value="전체">전체</option>';
        for entry in updated_values:
            html_string_selected += '<option value="{}">{}</option>'.format(entry['mname'], entry['mname'])

        return jsonify(html_string_selected=html_string_selected)


    # 상담글 작성
    def writeCounsel(self):
        title = request.form.get('inputTitle')
        big = request.form.get('SelectBigCate')
        mid = request.form.get('SelectMidCate')
        small = request.form.get('SelectSmallCate')
        question_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        question = request.form.get('inputContent')

        counsel = {'title': title, 'big_cate': big, 'mid_cate': mid, 'small_cate': small,
                   'question_date': question_date,
                   'question': question}
        counselingdao.setCounseling(counsel)
        result = counselingdao.getCounseling(question_date)
        return result


    # 태깅
    def getMorphs(self):
        title = request.form.get('inputTitle')
        question = request.form.get('inputContent')
        return getMorph(title+question)


    # 모델을 통한 예측
    def predictModel(self):
        big = request.form.get('SelectBigCate')

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


    def mobum_with_test(self):
        model = md.test_model(title, doc_list, data_recp_num, result2)
        model.weight_comp('파손 배송 제품 구매', weight=0.35, top=5)


counselController = CounselController()
