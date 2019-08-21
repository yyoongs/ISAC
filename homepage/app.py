from flask import Flask, render_template, request
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
    return render_template('solution.html')

# 테스트 (select)

@app.route('/test2')
def test2():
    upjong = counselingdao.getGijun()
    print(upjong)
    return render_template('test2.html', result=upjong, content_type='application/json')


if __name__ == '__main__':
    app.run()
