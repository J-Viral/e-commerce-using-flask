from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
app.config['MONGO_URI'] = 'mongodb+srv://jainviral19973:viral@cluster0.rbpj4f4.mongodb.net/myCollection'
mongo = PyMongo(app)




@app.route('/home')
def home():
    if 'username' in session:
        return render_template('index.html')
    return 

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            session['username'] = request.form['username']
            users.insert_one({'name': request.form['username'], 'password': hashed_password})
            return redirect(url_for('home'))
        else:
            flash('Username already exists. Please choose another.', 'error')

    return render_template('signup.html')

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})

        if login_user and bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
