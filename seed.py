from app import app
from models import db, Room

with app.app_context():
    db.session.add_all([
        Room(name="Room A", capacity=3),
        Room(name="Room B", capacity=2),
        Room(name="Room C", capacity=5)
    ])
    db.session.commit()
    print("Rooms added successfully!")
