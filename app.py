from flask import Flask, request, render_template, redirect, url_for, Response, jsonify
import cv2
app = Flask(__name__)

camera = cv2.VideoCapture(0)
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

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

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/our-work")
def ourwork():
    return render_template('ourwork.html')

@app.route('/done')
def done():
    if camera.isOpened():
        print("Releasing cam feed")
        camera.release()
    return jsonify("done")


app.run(debug = True)