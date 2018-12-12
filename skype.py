from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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


@app.route('/addcontact')
def addcontact():
    return render_template('addcontact.html')


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
                        print("fuck?")
                        session['username'] = username
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


#
# @app.route('/addcontactprocess', methods=['POST'])
# def addContactProcess():
#     if request.method == 'POST':
#         if 'username' in session:
#             username = session['username']
#             con = sqlite3.connect("skype")
#             print (username)
#             try:
#                 contact = request.form['contact']
#                 if contact:
#                     cur = con.cursor()
#                     myid = cur.execute("SELECT id FROM users WHERE username=?'' ", (username))
#                     toid = cur.execute("SELECT id FROM users WHERE username=?'' ", (contact))
#                     cur.execute("INSERT INTO contacts (from,to) VALUES(?,?)", (myid, toid))
#                     con.commit()
#                     return jsonify({'contact': contact})
#                 else:
#                     return jsonify({'error': 'Missing data!'})
#             except:
#                 con.rollback()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/list')
def list():
    con = sqlite3.connect("skype")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select id from users Where username= ? ", [session['username']])
    id = cur.fetchall()[0][0]
    cur.execute("select fromContact,toContact from contacts where fromContact= ?", [id])
    rows = cur.fetchall()
    idlist = [row[1] for row in rows]
    namelist = []
    for id in idlist:
        cur.execute("select username from users where id = ?", [id])
        namelist.append(cur.fetchall()[0][0])
    print(id)
    print(rows)
    # return "hello"
    # fetchet_rows = [row for row in rows if (row[0])]
    return render_template("list.html", rows=namelist)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(debug=True)
