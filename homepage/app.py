from flask import Flask, render_template, request
from module import counselingdao
from module.morph import getMorph
import pymysql
from keras.models import load_model
import json
import pandas as pd
import pickle

app = Flask(__name__)

class Database:
    def __init__(self):
        host = '133.130.122.150'
        user = "pingu"
        password = "datacampus12"
        db = "projectdb"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_counsel(self):
        self.cur.execute("SELECT counsel_id, big_cate, mid_cate, title FROM counsel LIMIT 50")
        result = self.cur.fetchall()
        return result

    def list_gijun(self):
        self.cur.execute("SELECT category_name FROM category cate, solution_gijun gijun where cate.id=gijun.id")
        result = self.cur.fetchall()
        return result

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

        # with open('searchModel/searchModel.lq', 'rb') as file:
        #     search = pickle.load(file)
        # print(search)

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
@app.route('/test')
def test():
    def db_query():
        db = Database()
        counsel = db.list_counsel()
        return counsel

    res = db_query()
    return render_template('test.html', result=res, content_type='application/json')

@app.route('/test2')
def test2():
    def db_query():
        db = Database()
        gijun = db.list_gijun()
        return gijun

    res = db_query()
    return render_template('test2.html', result=res, content_type='application/json')


if __name__ == '__main__':
    app.run()
