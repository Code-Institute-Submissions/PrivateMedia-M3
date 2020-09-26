import os
from flask import Flask, render_template, redirect, flash, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_toastr import Toastr 


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


@app.route('/login', methods=['POST'])
def register_users():
    users = mongo.db.Users
    users.insert(request.form.to_dict())
    flash("User Created", 'success')
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
