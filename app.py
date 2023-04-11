from flask import Flask, render_template, Response, request
import cv2
import time
from deepface import DeepFace
import os


app = Flask(__name__)

def capture_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # get the absolute path to the static folder
        static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
        # save the image to the static folder as capture.jpg
        filename = 'capture.jpg'
        filepath = os.path.join(static_folder, filename)
        cv2.imwrite(filepath, frame)
        time.sleep(10)
    cap.release()

def is_notInterested(img_address="static/capture.jpg"):
    img = cv2.imread(img_address)
    result = DeepFace.analyze(img, actions = ['emotion'])
    not_interested=(result['emotion']['angry']+result['emotion']['disgust']+result['emotion']['fear']+result['emotion']['sad'])/4
    interested=(result['emotion']['happy']+result['emotion']['suprise']+result['emotion']['neutral'])/3
    if interested<not_interested:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/image')
def image():
    return Response(open('static/capture.jpg', 'rb').read(), mimetype='image/jpeg')

@app.route('/save-image', methods=['POST'])
def save_image():
    image_data = request.data
    # save the image data to the static folder
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    filename = 'capture.jpg'
    filepath = os.path.join(static_folder, filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)
    return 'Image saved.'

@app.route('/check-interest')
def check_interest():
    not_interested = is_notInterested()
    return str(not_interested)


def run_flask():
    app.run(debug=False)
    
if __name__ == '__main__':
    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    capture_image()





 