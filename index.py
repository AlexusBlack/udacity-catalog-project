from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')
@app.route('/index', methods = ['GET'])
def index_route():
    return render_template('index.html', title='Starbase')


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)	