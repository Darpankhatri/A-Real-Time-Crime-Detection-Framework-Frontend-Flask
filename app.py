from flask import Flask,flash, request, render_template, redirect, url_for, Response, jsonify
import requests
import cv2
import logs
import os
from flask_mail import Mail, Message
from config import mailConfig, pusharConfig
from threading import Thread

app = Flask(__name__)

# set Log
app.logger.addHandler(logs.file_handler)
app.logger.setLevel(logs.logging.DEBUG)
# set Log

app.config.from_object(mailConfig)
mail = Mail(app)

app.secret_key = os.environ.get('SECRET_KEY')

def send_async_email(app, msg):
    try:
        with app.app_context():
            mail.send(msg)
    except Exception as e:
        app.logger.error("Email error"+str(e))

stop_camera = True

def gen_frames():
    global stop_camera
    camera = cv2.VideoCapture(0)
    while True:
        if stop_camera:
            break
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    camera.release()


@app.route("/")
def hello():
    return redirect(url_for('index'))

@app.route("/<name>")
def check(name):
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
    response = requests.post('http://192.168.205.17:5000/predict', json={'data': data})
    # Get the prediction from the response
    prediction = response.json()
    return prediction

    # Return the prediction as a string response
    return str(prediction)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['fileup']
        if file:
            print(file.filename)
            file.save('static/test/' + file.filename)  # Save the file to a desired location
            app.logger.info('file saved -> static/test/' + file.filename)
            file_img = file.filename
            print(file_img)
            # Send a POST request to the Flask API with the image file as data
            response = requests.post("http://192.168.52.209:5000/imgcheck", json={'file':file_img})
            prediction = response.json()
            app.logger.debug(prediction)
            
            # email
            email = request.form['email']
            if(email):
                print('yes')
                msg = Message('DOV Alert', sender ='info@dov.com', recipients = [email])
                msg.html = render_template('emails/alert_email.html', crimeClass=prediction)
                thr = Thread(target=send_async_email, args=[app, msg])
                thr.start()
        
            return str(prediction),200
        else:
            return jsonify({'message': 'File Not Found'}),404
        
    except Exception as e:
        app.logger.error(str(e))
        msg = str(e)
        return jsonify({'message':msg})
    

@app.route("/about")
def about():
    var1 = "Darpan"
    return render_template('about.html',varval = var1)

@app.route('/subscriber', methods=['POST'])
def subscriber():
    try:
        email = request.form['email']
        msg = Message('Subscribe DOV', sender =   'info@dov.com', recipients = [email])
        msg.html = render_template('emails/subscribe.html', content='Thanks for using!')
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        
        flash("Subscribe Successfully!", "success")
        return redirect(request.referrer)
        
    except Exception as e:
        app.logger.error(str(e))
        msg = str(e)
        
        flash("Something went wrong try again after 1 minute.", "error")
        return redirect(request.referrer)
        
    

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/predict")
def predict():
    return render_template('predict.html')

@app.route("/live-predict")
def predictlive():
    global stop_camera
    stop_camera = False
    return render_template('livepredict.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/our-work")
def ourwork():
    return render_template('ourwork.html')

@app.route("/pusher")
def pusher():
    return render_template('pusher.html')

@app.route("/alert")
def alert():
    return render_template('emails/alert_email.html',crimeClass="sdd")

@app.route('/done')
def done():
    # cv2.destroyAllWindows()
    msg = {
        "message": "Already Closed",
        "status": 0
    }
    
    global stop_camera
    if stop_camera == False:
        stop_camera = True
        msg = {
            "message": "Camera Closed",
            "status": 1            
        }
    pusharConfig.pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    return msg

@app.route('/startCamera')
def startCamera():
    app.logger.info("live")
    msg = {
        "message": "Camera start in few seconds.",
        "status": 1
    }
    try:
        response = requests.post("http://192.168.0.102:5000/liveCheck")
        app.logger.debug("Camera api response")
    except Exception as e:
        app.logger.error(str(e))
        
        msg["message"] = str(e)
        msg["status"] = 0
    
    return msg

app.run(debug = True)