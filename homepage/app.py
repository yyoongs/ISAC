from flask import Flask, render_template, request, jsonify
from myModule import counselingdao
from myModule.morpy import getMorph
from myModule.usado import searchAlgorithm
import pymysql
from keras.models import load_model
import json
import pandas as pd
import pickle

app = Flask(__name__)

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')


# 실시간 상담 처리
# GET, POST로만 접근 가능
@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        title = request.form.get('inputTitle')
        big = request.form.get('SelectBigCate')
        mid =request.form.get('SelectMidCate')
        small = request.form.get('SelectSmallCate')
        question = request.form.get('inputContent')
        counsel = {'title':title, 'big':big, 'mid':mid, 'small':small, 'question':question}
        counselingdao.setCounseling(counsel)
        result = counselingdao.getCounseling(title)

        # 태깅
        morphs = getMorph(title + question)
        print(morphs)

        with open('telecom_models/telecom_key_list.json', encoding='utf8') as f:
             List = json.load(f)

        model=load_model('telecom_models/telecom_광고서비스_add_paper.h5')
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        t = pd.DataFrame([[1 if _ in morphs else 0 for _ in List]])
        print(model.predict(t))

        with open('searchModel/searchModel.lq', 'rb') as file:
            search = pickle.load(file)

        # f = open('searchModel/searchModel.lq', 'rb')
        # search = pickle.load(f)
        # search = __name__()
        print(search)

        return render_template('result.html', result=result, morphs=morphs)


# 관련상담조회
@app.route('/relation')
def relation():
    return render_template('relation.html')

# 해결기준
@app.route('/solution')
def solution():
    upjong = counselingdao.getGijun()
    return render_template('solution.html', result=upjong)


@app.route('/_update_gijun')
def update_gijun():
    # 무슨 업종 선택했는지 가져오기
    selected_class = request.args.get('selected_class', type=str)

    # 업종에 해당하는 분쟁유형들 가져오기
    updated_values = counselingdao.getTrouble1(selected_class)

    # 분쟁유형 div에 분쟁유형들 넣기 / 전체는 기본
    html_string_selected = '<option value="">전체</option>'


    for entry in updated_values:
        print(entry['type_1'])
        html_string_selected += '<option value="{}">{}</option>'.format(entry['type_1'], entry['type_1'])

    print(html_string_selected)
    return jsonify(html_string_selected=html_string_selected)


if __name__ == '__main__':
    app.run()
