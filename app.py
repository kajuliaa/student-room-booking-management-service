from flask import Flask, render_template, redirect, url_for
from models import db, Room

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaidashova:123456789@localhost:5432/student_rooms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('index.html', rooms = rooms)
@app.route('/book/<int:room_id>', methods=['POST'])
def book(room_id):
    room = Room.query.get_or_404(room_id)
    if room.occupancy < room.capacity:
        room.occupancy +=1
        db.session.commit()
    return redirect(url_for('home'))