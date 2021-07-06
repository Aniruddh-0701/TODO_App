import webbrowser
from datetime import datetime
from os import error, urandom
from threading import Timer

from flask import Flask, redirect, render_template, request, session, url_for
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from werkzeug.wrappers import Response

from _pass import *

# App init
app = Flask(__name__)
app.secret_key = urandom(16)  # Secret key

# DB configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# Table manager classes

# ToDo table Manager
class Todo(db.Model):
    __tablename__ = "Tasks"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    user = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return "<Task %r>" % self.id


# Users table manager
class Users(db.Model):
    __tablename__ = "Users"
    _id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(16), nullable=False)


# Start directory
@app.route("/")
def index():
    if "username" in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for("login"))


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  # verify login details
        uid = request.form["uid"]
        pwd = hash(request.form["pwd"])
        try:
            user = Users.query.filter_by(_id=uid).first()
            if check_password(user.password, pwd):
                flash("Login successful", "success")
                session["username"] = user.username  # Set username on session
                return redirect(
                    url_for("tasks")
                )  # redirect to tasks page on successful login
            else:
                flash("InCorrect Username or Password", "error")
                3 / 0
        except:
            flash("User does not exist", "error")
            return render_template("login.html")
    return render_template("login.html")  # Loading Login page on GET method


# Logout
@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("index"))  # redirect to index page


# register
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        global userId
        userId = uid = request.form["uid"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        pwd = request.form["pwd"]
        try:
            assert Validator.validate_id(uid), "Invalid UID"
            assert Validator.validate_name(fname), "Invalid Name"
            assert Validator.validate_name(lname), "Invalid Name"
            assert Validator.validate_pwd(pwd), "Invalid password"
            epwd = encrypt_password(pwd)

            new_user = Users(_id=uid, username=fname + " " + lname, password=epwd)

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        except AssertionError as err:
            flash(err, "error")
            return render_template(
                "register.html", user_id=uid, fname=fname, lname=lname, pwd=pwd
            )
        except Exception:
            flash("Duplicate entry", "error")
            return render_template(
                "register.html", user_id=uid, fname=fname, lname=lname, pwd=pwd
            )
    else:
        return render_template("register.html", user_id="", fname="", lname="", pwd="")


# Check duplicate user id
@app.route("/check-duplicate/<uid>", methods=["POST"])
def check_duplicate(uid: str):
    userUnique = Users.query.get_or_404(uid)
    # print(userUnique)
    return "Already Exists", 200


# forgot password
@app.route("/forgot-password", methods=["GET", "POST"])
def forgotPwd():
    if request.method == "POST":
        global userId
        userId = request.form["uid"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        user = Users.query.filter_by(_id=userId).first()
        username = fname + " " + lname
        if user == None:
            return f"User ID does not exist"
        elif user.username == username:
            return redirect(url_for("reset"))
        else:
            return f"User Name does not exist"
    else:
        return render_template("forgot-password.html")


# reset password
@app.route("/reset-password", methods=["GET", "POST"])
def reset():
    global userId
    if request.method == "POST":
        userId = request.form["uid"]
        newPwd = request.form["pwd"]
        try:
            assert Validator.validate_pwd(newPwd), "Invalid Password"
        except AssertionError as err:
            flash(err, "error")
        user = Users.query.filter_by(_id=userId).first()
        user.password = encrypt_password(newPwd)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("reset-password.html", uId=userId)


# tasks page
@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    if request.method == "POST":
        task_txt = request.form["task"]
        task_ddl = datetime.strptime(request.form["deadline"], r"%Y-%m-%d")
        user = session["username"]
        newTask = Todo(content=task_txt, deadline=task_ddl, user=user)

        db.session.add(newTask)
        db.session.commit()
        return redirect("/tasks")

    else:
        tasks = (
            Todo.query.order_by(Todo.date_created)
            .filter_by(user=session["username"])
            .all()
        )
        return render_template("tasks.html", tasks=tasks)
        # except:
        #     return render_template("tasks.html")


# delete tasks
@app.route("/delete/<int:id>")
def delete(id: int):
    taskDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskDelete)
        db.session.commit()
        return redirect("/tasks")
    except:
        return "An error was encountered"


# update tasks
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    taskUpdate = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_content = request.form["task"]
        task_ddl = datetime.strptime(request.form["deadline"], r"%Y-%m-%d")
        # task = Todo.query.filter_by(id = id)
        taskUpdate.content = task_content
        taskUpdate.deadline = task_ddl
        db.session.commit()
        return redirect(url_for("tasks"))
    else:
        return render_template("update.html", task=taskUpdate)


# mark task as done
@app.route("/mark-as-done/<int:id>")
def markAsDone(id: int):
    taskDone = Todo.query.get_or_404(id)
    taskDone.completed = 1
    db.session.commit()
    return redirect(url_for("tasks"))


# mark task as pending
@app.route("/mark-as-pending/<int:id>")
def pending(id: int):
    taskPending = Todo.query.get_or_404(id)
    taskPending.completed = 0
    db.session.commit()
    return redirect(url_for("tasks"))


@app.route("/about")
def about():
    return render_template("about.html")


# Launch the app in browser
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/", new=1, autoraise=True)


if __name__ == "__main__":
    # Timer(1, open_browser).start()
    app.run(debug=True)
    # serve(app, listen="*:0701")
