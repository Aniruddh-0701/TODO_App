from flask import Flask, render_template, request
from models import Schema
import cgi
from Srevice import ToDoService

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('F1.html')


@app.route('/', methods=["POST"])
def res():
    global c
    c = 0
    s = request.form['Select']

    if s == "New":
        c += 1
        return render_template('Fe.html', s=s)
    if c == 0:
        return render_template('pass.html', s=s)
    else:
        req()


def req():
    s = "Sent"
    text = request.form['text']
    description = request.form['description']
    ddate = request.form['ddate']
    c(s, text, description, ddate)


@app.route('/')
def c(s, text, description, ddate):
    return render_template('pass.html', s=s, t=text, de=description, dd=ddate)

# l = [text, description, ddate]
# params = {'text': text, 'description': description, 'ddate': ddate}
# return ToDoService().create(params)


if __name__ == "__main__":
    Schema()

    app.run(debug=True)