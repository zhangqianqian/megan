from flask import Flask, url_for, request,render_template
app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('login.html')
        
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if len(request.form['username']) < len(request.form['password']):
            error = "username or password is wrong"
        else:
            error = "ok"
    else:
        return "error not support get request"
    return render_template('login.html', error=error)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
    #app.run()
