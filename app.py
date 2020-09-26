import os
from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_toastr import Toastr
import bcrypt


if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["MONGO_DBNAME"] = 'private_media'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)
toastr = Toastr(app)


@app.route('/')
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_users():
    if request.method == 'POST':
        users = mongo.db.Users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass, 'address' : request.form['address'], 'dob' : request.form['dob'],'hobbies' : request.form['hobbies'], 'events' : request.form['events']})
            session['username'] = request.form['username']
            flash("User Created", 'success')
            return redirect(url_for('login'))

        flash("Username Already Exist", 'error')

    return render_template('register.html')



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
