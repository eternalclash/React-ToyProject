
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

from datetime import datetime
## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    return render_template('detail.html')

## API 역할을 하는 부분
@app.route('/reservation', methods=['POST'])
def write_reservation():
    person_receive= request.form['person_give']
    checkIn_receive = request.form['checkIn_give']
    checkOut_receive = request.form['checkOut_give']
    room_receive = request.form['room_give']
    id_receive = request.form['id_give']

    doc = {
        'person': person_receive,
        'checkIn': checkIn_receive,
        'checkOut': checkOut_receive,
        'room': room_receive,
        'id': id_receive
    }

    db.reservation.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route('/reservation', methods=['GET'])
def reservation():
    reservations = list(db.reservation.find({}, {'_id': False}))
    return jsonify({'all_reservation': reservations})

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime=today.strftime('%Y-%m-%d-%H-%M-%S')

    filename=f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc={
        'title':title_receive,
        'content':content_receive,
        'file':f'{filename}.{extension}'
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
