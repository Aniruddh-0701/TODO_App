from flask import Flask, redirect, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0) # Currently unused
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    deadline = db.Column(db.DateTime)
    user = db.Column(db.String(100), nullable = False)

    def __repr(self):
        return '<Task %r>' % self.id

class Users(db.Model):
    __tablename__ = 'Users'
    _id = db.Column(db.String(50), primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(16), nullable = False)

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uid = request.form['uid']
        try:
            user = Users.query.filter_by(_id = uid).first()
            session['username'] = user['username']    
            # return redirect(url_for('tasks'))
        except:
            session['username'] = 'GUEST'
        finally: return redirect(url_for('tasks'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        uid = request.form['uid']
        fname = request.form['fname']
        lname = request.form['lname']
        pwd = request.form['pwd']
        new_user = Users(_id = uid, username = fname+' '+lname, password = pwd)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else: 
        return render_template('register.html')

@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        task_txt = request.form['task']
        task_ddl = datetime.strptime(request.form['deadline'], r'%Y-%m-%d')
        user = session['username']
        newTask = Todo(content = task_txt, deadline = task_ddl, user = user)

        db.session.add(newTask)
        db.session.commit()
        return redirect('/tasks') 
            
    else:
        try:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('tasks.html', tasks=tasks)
        except: 
            return render_template('tasks.html')

@app.route('/delete/<int:id>')
def delete(id):
    taskDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskDelete)
        db.session.commit()
        return redirect('/tasks')
    except:
        return 'An error was encountered'

if __name__=='__main__':
    app.run(debug=True)
