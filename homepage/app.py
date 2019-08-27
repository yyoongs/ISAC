from flask import Flask, render_template, request, redirect
from myModule.counselController import counselController
from myModule.gijunController import gijunController
from myModule.mobumController import mobumController
from flask import send_file, current_app as app
# from myModule.getSolutionController import getSolution

app = Flask(__name__)

# 메인 페이지
@app.route('/')
def index():
    return counselController.getBigcate()


@app.route('/_update_midCate')
def update_midCate():
    return counselController.updateMidcate()


@app.route('/_update_smallCate', methods=['GET'])
def update_smallCate():
    if request.method=='GET':
        big = request.args.get('selected_big', type=str)
        mid = request.args.get('selected_mid', type=str)
        return counselController.updateSmallcate(big, mid)


# 실시간 상담 처리
@app.route('/result', methods = ['POST'])
def writeCounsel():
    if request.method == 'POST':
        result, tags, gijun, cname = counselController.writeCounsel()
        model_res = counselController.predictModel(tags)
        result1,result2vec, finalResult = mobumController.getMobum()
        id=finalResult[0]
        title=finalResult[1]
        usado=finalResult[2]
        print(id, title, usado)

        return render_template('result.html',  result=result, tags=tags, gijun=gijun, cname=cname,  mobumList=zip(id, title, usado))


@app.route('/mobumCounsel/<id>')
def mobumCounsel(id):
    mobumResult = mobumController.getMobumContent(id)
    return render_template('mobumCounsel.html', result=mobumResult)


# ISAC 소개
@app.route('/show')
def show_static_pdf():
    return send_file('./static/Report.pdf')


# 해결기준
@app.route('/solution')
def solution():
    return gijunController.getGijun()


# 분쟁유형1
@app.route('/_update_trouble')
def update_gijun():
    return gijunController.updateTrouble1()

# 분쟁유형2 보여주기
@app.route('/_update_trouble2')
def update_trouble2():
    return gijunController.updateTrouble2()

# 분쟁유형3 보여주기
@app.route('/_update_trouble3')
def update_trouble3():
    return gijunController.updateTrouble3()

# 분쟁유형4 보여주기
@app.route('/_update_trouble4')
def update_trouble4():
    return gijunController.updateTrouble4()

@app.route('/_show_gijun_table', methods=['GET'])
def show_gijun_table():
    print('ㅎㅇㅎㅇ2')
    if request.method=='GET':
        print('ㅎㅇㅎㅇ')
        return gijunController.showGijunTable()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def Internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()