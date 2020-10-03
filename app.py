import os
from flask import Flask, render_template, redirect, flash, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_toastr import Toastr
from werkzeug.security import generate_password_hash, check_password_hash
import time


if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["MONGO_DBNAME"] = 'private_media'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)
toastr = Toastr(app)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/forgot-password')
def forgotPassword():
    return render_template('resetPassword.html')


@app.route('/')
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
                flash("Incorrect Username and/or Password", 'error')
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password", 'error')
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove username from session
    session.pop('username', None)
    return redirect(url_for('login'))


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
    active_user = mongo.db.users.find_one(
        {"username": session["user"]})

    users_post = mongo.db.posts.find()

    username = active_user["username"]

    if session["user"]:
        return render_template("index.html", username=username,
                               active_user=active_user, users_post=users_post)

    return redirect(url_for("index", username=username,
                            active_user=active_user))


@app.route("/resetPassword", methods=["GET", "POST"])
def resetPassword():
    if request.method == "POST":
        # Check username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            mongo.db.users.update({'_id': ObjectId(existing_user["_id"])},
            {
                "username": existing_user["username"],
                "password": generate_password_hash(
                            request.form.get("password")),
                "dob": existing_user["dob"],
                "address": existing_user["address"],
                "hobbies": existing_user["hobbies"],
                "events": existing_user["events"]
            })
            flash("Password Changed", 'success')
            return redirect(url_for("login"))
        else:
            # Username doesn't exist
            flash("Please Enter a valid Username", 'error')
            return redirect(url_for("forgotPassword"))

    return render_template("forgotPassword")


@app.route("/new_post/<user>", methods=["GET", "POST"])
def new_post(user):
    # Grab the session user's username from mongodb
    userMan = mongo.db.users.find_one(
            {"username": user})

    if userMan:
        upload_post = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "post": request.form.get("post"),
            "user_id": user
            }

        mongo.db.posts.insert_one(upload_post)
        flash("New Post!", 'success')
        return redirect(url_for("profile", username=user))

    return redirect(url_for("profile", username=user))


@app.route('/delete_post/<post_id>/<user>')
def delete_post(post_id, user):
    mongo.db.posts.remove({'_id': ObjectId(post_id)})
    flash("Deleted!", 'success')
    return redirect(url_for("profile", username=user, user=user))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)