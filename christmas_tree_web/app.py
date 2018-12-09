import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from watson_developer_cloud import VisualRecognitionV3, WatsonApiException
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer,String

app = Flask(__name__, instance_relative_config=True)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)
app.config.from_pyfile('config.cfg', silent=True)
#GOOGLE_MAP_API_KEY = app.config['SECRET_KEY']
GOOGLE_MAP_API_KEY = app.config['GOOGLE_MAP_API_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///place.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Place(db.Model):
    id = Column(Integer, primary_key=True)
    longitude = Column(Integer)
    latitude = Column(Integer)
    score = Column(Integer)

    def __init__(self, longitude, latitude, score):
        self.longitude = longitude
        self.latitude = latitude
        self.score = score
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def analise_image(image_file_path):
    visual_recognition = VisualRecognitionV3(
        version=app.config["WATSON_API_VERSION"],
        iam_apikey=app.config["WATSON_API_KEY"]
    )
    visual_recognition.set_detailed_response(True)

    try:
        with open(image_file_path, mode="rb") as f:
            classes = visual_recognition.classify(f)
            json_dictionary = classes.get_result()
            if "code" not in json_dictionary:
                if "christmas_tree" not in json_dictionary:
                    return 0
                else:
                    return int(json_dictionary["christmas_tree"])

            else:
                status_code = classes.get_status_code()
                print(str(status_code))
                raise ConnectionAbortedError

    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        raise ConnectionAbortedError

def add_place(place,longitude,latitude,score):
    places = Place(longitude,latitude,score)
    db.session.add(places)
    db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        place = request.form["place"]
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img_file.save(file_path)
            img_url = '/uploads/' + filename
            result = analise_image(str(file_path))
            add_place(place,100,100,result)
            return render_template('result.html', img_url=img_url,result=result,place=place,google_map_api_key=GOOGLE_MAP_API_KEY)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/result')
def result():
    google_map_api_key = app.config["GOOGLE_MAP_API_KEY"]
    return render_template('result.html',google_map_api_key=google_map_api_key)


if __name__ == '__main__':
    app.debug = True
    app.run()
