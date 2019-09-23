from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.secret_key = 'mysecretss'
app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb://kihara:kihara@ds151752.mlab.com:51752/bktlist'
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'hello '+ session['firstname'] +' '+ session['lastname'] + '. Email: ' + session['email'] +' '+ render_template('authorized.html')
    return render_template('index.html')
    

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name':request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            session['firstname'] = login_user['firstname']
            session['lastname'] = login_user['lastname']
            session['email'] = login_user['email']
            return redirect(url_for('index'))

    return 'Invalid username or password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name':request.form['username'], 'password': hashpass,'email':request.form['email'],'firstname':request.form['firstname'],'lastname':request.form['lastname']})
            session['username'] = request.form['username']
            session['firstname'] = request.form['firstname']
            session['lastname'] = request.form['lastname']
            session['email'] = request.form['email']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=80)