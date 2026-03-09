from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import os

app = Flask(__name__)


# ----------------------------
# DATABASE INITIALIZATION
# ----------------------------

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS meetings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        leader TEXT,
        client_name TEXT,
        designation TEXT,
        organisation TEXT,
        opportunity_size TEXT
    )
    """)

    conn.commit()
    conn.close()


# Run database initialization when app loads
init_db()


# ----------------------------
# TECHM LEADER LIST
# ----------------------------

leaders = [
    "Mohit Joshi",
    "Manish Mangal",
    "Harshul Asnani",
    "Jena",
    "Sandeep",
    "Harsh",
    "Dom",
    "Gaurav",
    "Praveen",
    "Ashwini",
    "Swaapnil",
    "Arun",
    "Vasu",
    "Hridey"
]


# ----------------------------
# HOME PAGE
# ----------------------------

@app.route("/")
def home():

    dates = ["2 March", "3 March", "4 March"]

    times = []

    for hour in range(9, 18):
        times.append(f"{hour}:00-{hour}:30")
        times.append(f"{hour}:30-{hour+1}:00")

    return render_template(
        "index.html",
        dates=dates,
        times=times,
        leaders=leaders
    )


# ----------------------------
# CHECK AVAILABLE LEADERS
# ----------------------------

@app.route("/available_leaders")
def available_leaders():

    date = request.args.get("date")
    time = request.args.get("time")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "SELECT leader FROM meetings WHERE date=? AND time=?",
        (date, time)
    )

    booked = [row[0] for row in c.fetchall()]

    conn.close()

    available = [l for l in leaders if l not in booked]

    return jsonify({"leaders": available})


# ----------------------------
# BOOK MEETING
# ----------------------------

@app.route("/book", methods=["POST"])
def book():

    date = request.form["date"]
    time = request.form["time"]
    leader = request.form["leader"]
    client = request.form["client"]
    designation = request.form["designation"]
    organisation = request.form["organisation"]
    opportunity = request.form["opportunity"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO meetings
    (date, time, leader, client_name, designation, organisation, opportunity_size)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, time, leader, client, designation, organisation, opportunity))

    conn.commit()
    conn.close()

    return redirect("/")


# ----------------------------
# START APP
# ----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
