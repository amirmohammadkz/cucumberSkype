from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/login')
def login():
    return render_template('login.html')


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
        con = sqlite3.connect("skype")
        username = request.form['username']
        password = request.form['password']

        if username and password:
            try:
                cur = con.cursor()
                cur.execute("SELECT username, password FROM users")
                users = cur.fetchall()
                user = [i for i in users if i[0] == username]
                if (len(user) > 0):
                    if (str(user[0][1]) == password):
                        return jsonify({'name': username})
                    else:
                        return jsonify({'error': 'username or password is incorrect!'})
                else:
                    return jsonify({'error': 'username or password is incorrect!'})
                # con.commit()
            except Exception as e:
                print(e)
                return jsonify({'error': 'something went wrong!'})
            finally:
                con.close()


if __name__ == '__main__':
    app.run(debug=True)
