import os
from flask import (
    Flask, render_template, redirect, flash, request, url_for, session)
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
    else:
        if session.get('user') is not None:
            return redirect(url_for("profile", username=session["user"]))
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove username from session
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # Informs the user that username already exis
        if existing_user:
            flash("Username already exists", 'error')
            return redirect(url_for("register"))

        # creates a new user
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "secret": request.form.get("secret").lower(),
            "dob": request.form.get("dob").lower(),
            "address": request.form.get("address").lower(),
            "hobbies": request.form.get("hobbies").lower(),
            "events": request.form.get("events").lower()
        }
        mongo.db.users.insert_one(register)

        # Put new user into a session cookie
        session['user'] = request.form.get("username").lower()
        flash("Registration Successful!", 'success')
        return redirect(url_for("login", username=session["user"]))

    return render_template("register.html")


# Profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # verifying if there is an existing user session
    if session.get("user") is None:
        return redirect(url_for("login", username=username))
    if username != session['user']:
        return redirect(url_for("profile", username=session['user']))

    # Grab the session user's username from mongodb
    active_user = mongo.db.users.find_one(
        {"username": session["user"]})

    # returns the most recent user post
    username = active_user["username"]
    user_post = mongo.db.posts.find({"user_id":
                                    session["user"]}).sort("_id", -1)

    return render_template("index.html", username=username,
                           active_user=active_user,
                           user_post=user_post)


@app.route("/resetPassword", methods=["GET", "POST"])
def resetPassword():
    if request.method == "POST":
        # Check username exists in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # defining user secret from mongo
        secret = existing_user["secret"]
        # retrieving user inputed secrete
        user_secret = request.form.get("secret").lower()

        # checking user inputed secret matches user secret in db
        if existing_user and (user_secret == secret):
            # Ensure hashed password matches user input
            mongo.db.users.update({'_id': ObjectId(existing_user["_id"])},
            {
                "username": existing_user["username"],
                "password": generate_password_hash(
                            request.form.get("password")),
                "secret": existing_user["secret"],
                "dob": existing_user["dob"],
                "address": existing_user["address"],
                "hobbies": existing_user["hobbies"],
                "events": existing_user["events"]
            })
            flash("Password Changed", 'success')
            return redirect(url_for("login"))
        else:
            # no match found username and secrete
            flash("No Match Found", 'error')
            return redirect(url_for("forgotPassword"))

    return render_template("forgotPassword")


@app.route("/new_post/<user>", methods=["GET", "POST"])
def new_post(user):
    # Grab the session user's username from mongodb
    session_user = mongo.db.users.find_one(
            {"username": user})

    if session_user:
        upload_post = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "post": request.form.get("post"),
            # one to many entity type reference
            "user_id": user
            }
        # Insert new post
        mongo.db.posts.insert_one(upload_post)
        flash("New Post!", 'success')
        return redirect(url_for("profile", username=user))

    return redirect(url_for("profile", username=user))


@app.route('/delete_post/<post_id>/<user>')
def delete_post(post_id, user):
    mongo.db.posts.remove({'_id': ObjectId(post_id)})
    flash("Deleted!", 'success')
    return redirect(url_for("profile", username=user, user=user))


@app.route('/edit_post/<post_id>/<user>')
def edit_post(post_id, user):
    return render_template('editPost.html',
                           current_post=mongo.db.posts.find_one(
                              {'_id': ObjectId(post_id)}),
                           post_id=post_id, user=user)


@app.route('/update_post/<post_id>/<user>', methods=["GET", "POST"])
def update_post(post_id, user):
    mongo.db.posts.update(
        {'_id': ObjectId(post_id)},
        {'post': request.form.get('post_content'),
         "date": time.strftime("%Y-%m-%d %H:%M"),
         "user_id": user})
    flash("Updated!", 'success')

    return redirect(url_for("profile", username=user, user=user,
                            ))


@app.route('/edit_profile/<profile_id>/<user>')
def edit_profile(profile_id, user):
    return render_template('updateProfile.html',
                           current_profile=mongo.db.users.find_one(
                              {'_id': ObjectId(profile_id)}),
                           profile_id=profile_id, user=user
                           )


@app.route('/update_profile/<profile_id>/<user>', methods=["GET", "POST"])
def update_profile(profile_id, user):
    mongo.db.users.update(
        {'_id': ObjectId(profile_id)},
        {"username": request.form.get("username").lower(),
            "password": generate_password_hash(
                            request.form.get("password")),
            "secret": request.form.get("secret").lower(),
            "dob": request.form.get("dob").lower(),
            "address": request.form.get("address").lower(),
            "hobbies": request.form.get("hobbies").lower(),
            "events": request.form.get("events").lower()})
    flash("Updated!", 'success')

    return redirect(url_for("profile", username=user
                            ))


@app.route('/delete_profile/<profile_id>')
def delete_profile(profile_id):
    mongo.db.users.remove({'_id': ObjectId(profile_id)})
    flash("User Deleted!", 'success')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
