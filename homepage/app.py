from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        title = request.form.get('inputTitle')
        big = request.form.get('SelectBigCate')
        mid =request.form.get('SelectMidCate')
        small = request.form.get('SelectSmallCate')
        situation = request.form.get('SelectSituation')
        content = request.form.get('inputContent')
        return render_template('result.html',  title=title, big=big, mid=mid, small=small, situation=situation, content=content)
#        return(str(big+' '+mid+' '+small))
#        return render_template("result.html", result=result)
 #   return render_template('result.html')


@app.route('/custom')
def custom():
    return render_template('custom.html')


@app.route('/relation')
def relation():
    return render_template('relation.html')


@app.route('/rightnow')
def rightnow():
    return render_template('rightnow.html')

@app.route('/solution')
def solution():
    return render_template('solution.html')

if __name__ == '__main__':
    app.run()
