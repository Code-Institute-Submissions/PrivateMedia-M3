import os
from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_toastr import Toastr
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["MONGO_DBNAME"] = 'private_media'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)
toastr = Toastr(app)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
               existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # Invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password", 'error')
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists", 'error')
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "dob": request.form.get("dob").lower(),
            "address": request.form.get("address").lower(),
            "hobbies": request.form.get("hobbies").lower(),
            "events": request.form.get("events").lower()


        }
        mongo.db.users.insert_one(register)

        # Put new user into a session cookie
        session['user'] = request.form.get("username").lower()
        flash("Registration Successful!", 'success')
        return redirect(url_for("login", username=session["username"]))

    return render_template("register.html")


# Profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Grab the session user's username from mongodb
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    address = mongo.db.users.find_one(
        {"username": session["user"]})["address"]

    dob = mongo.db.users.find_one(
        {"username": session["user"]})["dob"]

    events = mongo.db.users.find_one(
        {"username": session["user"]})["events"]

    hobbies = mongo.db.users.find_one(
        {"username": session["user"]})["hobbies"]

    events = mongo.db.users.find_one(
        {"username": session["user"]})["events"]

    if session["user"]:
        return render_template("index.html", username=username, address=address, dob=dob, events=events, hobbies=hobbies)

    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
