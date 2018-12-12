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

@app.route('/addcontact')
def addcontact(): 
    return render_template('addcontact.html')

@app.route('/loginProcess', methods=['POST'])
def loginProcess():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            return jsonify({'name': username})
        else:
            return jsonify({'error': 'Missing data!'})

@app.route('/addcontactprocess', methods=['POST'])
def addContactProcess():
    if request.method == 'POST':
        con = sqlite3.connect("skype")
        try:
            contact = request.form['contact']
            if contact:
                cur = con.cursor()
                myid = cur.execute("SELECT id FROM users WHERE username=?'' ",(username))
                toid = cur.execute("SELECT id FROM users WHERE username=?'' ",(contact))
                cur.execute("INSERT INTO contacts (from,to) VALUES(?,?)", (myid, toid))
                con.commit()
                return jsonify({'contact': contact})
            else:
                return jsonify({'error': 'Missing data!'})
        except:
            con.rollback()

if __name__ == '__main__':
    app.run(debug=True)
