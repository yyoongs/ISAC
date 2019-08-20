from flask import Flask, render_template, request
from dao import counselingdao
import pymysql

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
        situation = request.form.get('SelectSituation')
        question = request.form.get('inputContent')
        counsel = {'title':title, 'big':big, 'mid':mid, 'small':small, 'situation':situation,'question':question}
        counselingdao.setCounseling(counsel)
        # print(counsel_id)
        result = counselingdao.getCounseling(title)
        print(result)

        return render_template('result.html', result=result)


# 고객센터
@app.route('/custom')
def custom():
    return render_template('custom.html')

# 관련상담조회
@app.route('/relation')
def relation():
    return render_template('relation.html')

# 실시간 상담 조회
@app.route('/rightnow')
def rightnow():
    return render_template('rightnow.html')

# 해결기준
@app.route('/solution')
def solution():
    return render_template('solution.html')



if __name__ == '__main__':
    app.run()
