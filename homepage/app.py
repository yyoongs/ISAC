from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('resultpage.html')


@app.route('/custom')
def custom():
    return render_template('custom.html')


@app.route('/relation')
def relation():
    return render_template('relation.html')


@app.route('/rightnow')
def rightnow():
    return render_template('rightnow.html')


if __name__ == '__main__':
    app.run()
