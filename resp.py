from flask import Flask, render_template, request

resp = Flask(__name__)


@resp.route("/")
def index():
    return render_template('F1.html')


@resp.route('/', methods=["Post"])
def res():
    s = request.form["Select"]
    if s=="New":
        return render_template('Fe.html')
    else:
        return render_template('pass.html', s=s)


resp.run(debug=True)
