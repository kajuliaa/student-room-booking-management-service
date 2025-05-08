import sqlite3

conn = sqlite3.connect('bookings.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS rooms (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          capacity INTEGER,
          occupancy INTEGER) ''')

rooms =[
    ('Room A', 3, 0),
    ('Room B', 2, 0)
]

c.executemany('INSERT INTO rooms (name, capacity, occupancy) VALUES (?, ?,?)', rooms)

conn.commit()
conn.close()