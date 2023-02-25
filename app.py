from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/<name>")
def check(name):
    # return f"hello {name}"
    return redirect(url_for('about'))

@app.route("/about")
def about():
    var1 = "Darpan"
    
    # return "Index1"
    return render_template('about.html',varval = var1)


@app.route("/index")
def index():
    return render_template('index.html')

app.run(debug = True)