from flask import Flask, request, render_template, redirect, url_for, Response, jsonify
import requests
import cv2
import logs

app = Flask(__name__)

# set Log
app.logger.addHandler(logs.file_handler)
app.logger.setLevel(logs.logging.DEBUG)
# set Log

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

@app.route('/predictApi', methods=['GET'])
def predictApi():
    data = [
        "The quick brown fox jumps over the lazy cat.",
        "The sun shines through the leaves of the tree.",
        "The lazy dog",
        "The dog sleeps in the shade of the tree."
    ]

    # Send a POST request to the Jupyter notebook API
    response = requests.post('http://10.11.63.5:5000/predict&#39', json={'data': data})

    # Get the prediction from the response
    prediction = response.json()

    # Return the prediction as a string response
    return str(prediction)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['fileup']
    if file:
        print(file.filename)
        file.save('static/test/' + file.filename)  # Save the file to a desired location
        app.logger.info('file saved -> static/test/' + file.filename)
        with open('static/test/'+ file.filename, 'rb') as file:
            # Create a dictionary to hold the file data
            files = {'image': file}
            
            # Send a POST request to the Flask API with the image file as data
            # response = requests.post("url", files=files)
        data = {
            'message': 'Image uploaded and saved successfully',
            'success': True
        }
    else:
        data = {
            'message': 'File Not Found',
            'success': False
        }

    return jsonify(data)

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