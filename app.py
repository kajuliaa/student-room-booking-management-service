from flask import Flask, render_template, redirect, url_for, request, url_for
from models import db, Room, Booking, User
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaidashova:123456789@localhost:5432/student_rooms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Setup Falsk Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create Auth Routes
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email= request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('index.html', rooms = rooms)

@app.route('/book', methods=['POST'])
@login_required
def book():
    room_id = int(request.form['room_id'])
    start = datetime.fromisoformat(request.form['start'])
    end= datetime.fromisoformat(request.form['end'])
    

    overlapping_count = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.end_time > start,   
        Booking.start_time < end    
    ).count()

    # Check if there are free places and booking the next one
    room = Room.query.get_or_404(room_id)
    if overlapping_count <room.capacity:
        # Create booking
        new_booking = Booking(room_id = room_id, start_time= start, end_time= end, user_id = current_user.id)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return 'Room is full for that time, choose another one', 400

if __name__ == '__main__':
    app.run(debug=True)

    


    
#TODO Check if register data are commiting 
#TODO Trying to login