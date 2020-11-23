from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0) # Currently unused
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    deadline = db.Column(db.DateTime)

    def __repr(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_txt = request.form['task']
        task_ddl = datetime.strptime(request.form['deadline'], r'%Y-%m-%d')
        newTask = Todo(content = task_txt, deadline = task_ddl)

        db.session.add(newTask)
        db.session.commit()
        return redirect('/') 
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    taskDelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(taskDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'An error was encountered'

if __name__=='__main__':
    app.run(debug=True)
