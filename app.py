from flask import Flask, render_template, redirect, url_for, request, url_for
from models import db, Room, Booking
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaidashova:123456789@localhost:5432/student_rooms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('index.html', rooms = rooms)

@app.route('/book', methods=['POST'])
def book():
    room_id = int(request.form['room_id'])
    start = datetime.fromisoformat(request.form['start'])
    end= datetime.fromisoformat(request.form['end'])
    
    # 1. Check for overlapping bookings
    overlapping = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.end_time > start,   # Existing booking ends *after* requested start
        Booking.start_time < end    # Existing booking starts *before* requested end
    ).first()

    if overlapping:
        return f'This time slot is already booked for Room {room_id}!', 400

    
    # Create booking
    new_booking = Booking(room_id = room_id, start_time= start, end_time= end)
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for('home'))


    
