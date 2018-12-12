from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/signup')
def login():
    return render_template('signup.html')


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        con = sqlite3.connect("skype")
        try:
            username = request.form['username']
            password = request.form['password']

            if username and password:
                # with sqlite3.connect("skype") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username,password) VALUES(?,?)", (username, password))
                con.commit()
                return jsonify({'name': username})
            else:
                return jsonify({'error': 'Missing data!'})
        except:
            con.rollback()
        finally:
            con.close()

@app.route('/loginProcess', methods=['POST'])
def loginProcess():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            return jsonify({'name': username})
        else:
            return jsonify({'error': 'Missing data!'})

if __name__ == '__main__':
    app.run(debug=True)
