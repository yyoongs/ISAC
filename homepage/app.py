from flask import Flask, render_template, request
from datetime import datetime
from myModule import counselingdao
from myModule.counselController import counselController
from myModule.gijunController import gijunController
from myModule.morpy import getMorph
from myModule.usado import searchAlgorithm
import pymysql
from keras.models import load_model
import json
import pandas as pd
import pickle
import models
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://pingu:datacampus12@133.130.122.150/ISAC"
# mydb = SQLAlchemy(app)


# 메인 페이지
@app.route('/')
def index():
    return counselController.getBigcate()
    # bigCate = counselingdao.getBigCate()
    # return render_template('index.html', big_cate=bigCate)

@app.route('/_update_midCate')
def update_midCate():
    # print(data)
    return counselController.updateMidcate()


# 실시간 상담 처리
@app.route('/result', methods = ['POST'])
def writeCounsel():
    if request.method == 'POST':
        result = counselController.writeCounsel()
        morphs = counselController.getMorphs()
        counselController.predictModel()
        counselController.mobum_with_test()

        return render_template('result.html', result=result, morphs=morphs)


# 관련상담조회
@app.route('/relation')
def relation():
    return render_template('relation.html')

# 해결기준
@app.route('/solution')
def solution():
    # return render_template('solution.html')
    return gijunController.getGijun()


@app.route('/_update_gijun')
def update_gijun():
    # print(data)
    return gijunController.updateTrouble()


@app.route('/_show_gijun_table')
def show_gijun_table():
    return gijunController.showGijunTable()
    # selected_upjong = request.args.get('selected_class', type=str)
    # selected_trouble1 = request.args.get('selected_entry', type=str)
    # result = counselingdao.getStandardBigo(selected_upjong, selected_trouble1)
    #
    # print(result)
    # # print(jsonify(result))
    #
    # # 방법 1
    # return jsonify(datas= result)

    # 방법 2
    # return render_template('solution.html', datas=result)



if __name__ == '__main__':
    app.run()
