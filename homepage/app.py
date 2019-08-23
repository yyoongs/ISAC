from flask import Flask, render_template, request
from myModule.counselController import counselController
from myModule.gijunController import gijunController


app = Flask(__name__)


# 메인 페이지
@app.route('/')
def index():
    return counselController.getBigcate()

@app.route('/_update_midCate')
def update_midCate():
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
    return gijunController.getGijun()


@app.route('/_update_gijun')
def update_gijun():
    # print(data)
    return gijunController.updateTrouble()


@app.route('/_show_gijun_table')
def show_gijun_table():
    return gijunController.showGijunTable()


if __name__ == '__main__':
    app.run()
