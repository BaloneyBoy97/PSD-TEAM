#!/usr/bin/env python3
import sqlite3

# Create a new db named appdata
conn = sqlite3.connect("appdata.db")
curr = conn.cursor()

# Create user data table to store user information
curr.execute("""
CREATE TABLE IF NOT EXISTS userdata(
    userid INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    isAdmin BOOLEAN NOT NULL DEFAULT 0
)
""")
# Create flights table to store flight information
curr.execute("""
CREATE TABLE IF NOT EXISTS flights(
    flightid INTEGER PRIMARY KEY,
    flightnumber TEXT UNIQUE NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departuretime TEXT NOT NULL,
    arrivaltime TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
# Create bookings table to store user booking data
curr.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    bookingid INTEGER PRIMARY KEY,
    userid INTEGER,
    flightid INTEGER,
    FOREIGN KEY (userid) REFERENCES userdata(userid),
    FOREIGN KEY (flightid) REFERENCES flights(flightid)
)
""")

# Sample data for userdata table
sample_userdata = [
    ('john.doe@example.com', 'JohnDoe', 'password123', 0),
    ('jane.smith@example.com', 'JaneSmith', 'pass456', 0),
    ('admin@example.com', 'Admin', 'adminpass', 1),
    ('mike.jones@example.com', 'MikeJones', 'mike789', 0),
    ('alice.brown@example.com', 'AliceBrown', 'alice987', 0),
    ('charlie.davis@example.com', 'CharlieDavis', 'charlie654', 0),
    ('david.evans@example.com', 'DavidEvans', 'david321', 0),
    ('eve.foster@example.com', 'EveFoster', 'eve111', 0),
    ('frank.green@example.com', 'FrankGreen', 'frank222', 0),
    ('grace.harris@example.com', 'GraceHarris', 'grace333', 0),
    ('henry.ingham@example.com', 'HenryIngham', 'henry444', 0),
    ('ivy.johnson@example.com', 'IvyJohnson', 'ivy555', 0),
    ('jack.king@example.com', 'JackKing', 'jack666', 0),
    ('kate.lee@example.com', 'KateLee', 'kate777', 0),
    ('leo.martin@example.com', 'LeoMartin', 'leo888', 0)
]

# Sample data for flights table
sample_flights = [
    ('AA100', 'New York', 'Los Angeles', '2024-06-01 08:00:00', '2024-06-01 11:00:00', 'Scheduled'),
    ('BA200', 'London', 'New York', '2024-06-02 09:00:00', '2024-06-02 12:00:00', 'Scheduled'),
    ('CA300', 'Beijing', 'San Francisco', '2024-06-03 10:00:00', '2024-06-03 13:00:00', 'Scheduled'),
    ('DA400', 'Dubai', 'Sydney', '2024-06-04 11:00:00', '2024-06-04 14:00:00', 'Scheduled'),
    ('EA500', 'Paris', 'Tokyo', '2024-06-05 12:00:00', '2024-06-05 15:00:00', 'Scheduled'),
    ('FA600', 'Frankfurt', 'Chicago', '2024-06-06 13:00:00', '2024-06-06 16:00:00', 'Scheduled'),
    ('GA700', 'Hong Kong', 'San Francisco', '2024-06-07 14:00:00', '2024-06-07 17:00:00', 'Scheduled'),
    ('HA800', 'Toronto', 'Vancouver', '2024-06-08 15:00:00', '2024-06-08 18:00:00', 'Scheduled'),
    ('IA900', 'Delhi', 'London', '2024-06-09 16:00:00', '2024-06-09 19:00:00', 'Scheduled'),
    ('JA1000', 'Madrid', 'Buenos Aires', '2024-06-10 17:00:00', '2024-06-10 20:00:00', 'Scheduled'),
    ('KA1100', 'Rome', 'Dubai', '2024-06-11 18:00:00', '2024-06-11 21:00:00', 'Scheduled'),
    ('LA1200', 'Johannesburg', 'Cairo', '2024-06-12 19:00:00', '2024-06-12 22:00:00', 'Scheduled'),
    ('MA1300', 'Mexico City', 'Miami', '2024-06-13 20:00:00', '2024-06-13 23:00:00', 'Scheduled'),
    ('NA1400', 'Sao Paulo', 'Lisbon', '2024-06-14 21:00:00', '2024-06-15 00:00:00', 'Scheduled'),
    ('OA1500', 'Bangkok', 'Sydney', '2024-06-15 22:00:00', '2024-06-16 01:00:00', 'Scheduled')
]

# Sample data for bookings table
sample_bookings = [(i+1, i+1) for i in range(15)]

# Insert sample data into userdata table
curr.executemany("INSERT INTO userdata (email, username, password, isAdmin) VALUES (?, ?, ?, ?)", sample_userdata)

# Insert sample data into flights table
curr.executemany("INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status) VALUES (?, ?, ?, ?, ?, ?)", sample_flights)

# Insert sample data into bookings table
curr.executemany("INSERT INTO bookings (userid, flightid) VALUES (?, ?)", sample_bookings)

# Commit changes and close connection
conn.commit()
conn.close()
