from flask import Flask, request, render_template, redirect, url_for
# import cv2
app = Flask(__name__)

@app.route("/")
def hello():
    return redirect(url_for('index'))

@app.route("/<name>")
def check(name):
    # return f"hello {name}"
    return redirect(url_for('about'))

@app.route("/about")
def about():
    var1 = "Darpan"
    return render_template('about.html',varval = var1)


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/predict")
def predict():
    return render_template('predict.html')

@app.route("/live-predict")
def predictlive():
    return render_template('livepredict.html')


@app.route("/our-work")
def ourwork():
    return render_template('ourwork.html')

app.run(debug = True)