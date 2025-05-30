import sqlite3
import tkinter as tk
from tkinter import messagebox

def book_room(room_id):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    c. execute('SELECT capacity, occupancy FROM rooms WHERE id=?', (room_id,))
    result = c.fetchone()
    if result:
        capacity, occupancy = result
        if occupancy< capacity:
            c.execute("UPDATE rooms SET occupancy =occupancy+1 WHERE id =?", (room_id,))
            conn.commit()
            messagebox.showinfo('Success', 'Room booked!')
        else:
            messagebox.showwarning('Full', "Room is full!")
    conn.close()
    refresh_rooms()

def refresh_rooms():
    for widget in frame.winfo_children():
        widget.destroy()
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT id, name, capacity, occupancy FROM rooms")
    for row in c.fetchall():
        room_id, name, cap, occ = row
        label = tk.Label(frame, text=f"{name}: {occ}/{cap}")
        label.pack()
        btn = tk.Button(frame, text="Book", command=lambda id=room_id: book_room(id))
        btn.pack()
    conn.close()

root = tk.Tk()
root.title("Student Room Booking")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

refresh_rooms()

root.mainloop()