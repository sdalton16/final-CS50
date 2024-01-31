from flask import Flask, render_template, request, session, redirect, url_for
import os
from flask_session import Session
import json
import sqlite3
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def select_game_mode():

    if session.get("user_id") is None:
            return redirect("/login")

    if request.method == "POST":
        game = request.form.get("game_select")
        if game == "Addition & Subtraction":
            return redirect("/add_sub")
        if game == "Multiplication & Division":
            return redirect("/multiply_divide")

    else:
        return render_template("game_select.html")

@app.route("/add_sub", methods=["GET", "POST"])
def mode_add_sub():

    if session.get("user_id") is None:
            return redirect("/login")

    if request.method == "POST":
        game_mode = "add_sub"
        user = session["user_id"]

        saved_game = int(request.get_json())

        now = datetime.now()
        date = now.strftime("%D%m%y")

        data_to_save = [user,game_mode,saved_game,date]

        conn = sqlite3.connect("math.db")
        db = conn.cursor()
        db.executemany("INSERT INTO leaderboard VALUES(?, ?, ?, ?)", [data_to_save])
        conn.commit()
        conn.close()

        return redirect("/")

    else:
        return render_template("add_sub.html")


@app.route("/multiply_divide", methods=["GET", "POST"])
def mode_multiply_divide():

    if session.get("user_id") is None:
            return redirect("/login")

    if request.method == "POST":
        game_mode = "multiply_divide"
        user = session["user_id"]

        saved_game = int(request.get_json())

        now = datetime.now()
        date = now.strftime("%D%m%y")

        data_to_save = [user,game_mode,saved_game,date]

        conn = sqlite3.connect("math.db")
        db = conn.cursor()
        db.executemany("INSERT INTO leaderboard VALUES(?, ?, ?, ?)", [data_to_save])
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("multiply_divide.html")

@app.route("/leaderboard", methods=["GET"])
def leaderboard():

    if session.get("user_id") is None:
            return redirect("/login")

    add_sub = "add_sub"
    multiply_divide = "multiply_divide"

    conn = sqlite3.connect("math.db")
    db = conn.cursor()
    db.row_factory = sqlite3.Row
    add_sub_leaders = db.execute("SELECT user, score, date FROM leaderboard WHERE game_mode = ? ORDER BY score DESC LIMIT 3", (add_sub,)).fetchall()
    mulitply_divide_leaders = db.execute("SELECT user, score, date FROM leaderboard WHERE game_mode = ? ORDER BY score DESC LIMIT 3", (multiply_divide,)).fetchall()
    conn.close()

    return render_template("leaderboard.html", add_sub_leaders=add_sub_leaders, multiply_divide_leaders=mulitply_divide_leaders)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            notice = "Must provide a username!"
            return render_template("login.html", notice=notice)

        if not request.form.get("password"):
            notice = "Must provide a password!"
            return render_template("login.html", notice=notice)

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("math.db")
        db = conn.cursor()
        db.row_factory = sqlite3.Row

        user_data = db.execute("SELECT user, password FROM users WHERE user = ?", (username,)).fetchall()

        if len(user_data) != 1 or not check_password_hash(user_data[0]["password"], password):
            notice = "Invalid username or password!"
            return render_template("login.html", notice=notice)

        session["user_id"] = user_data[0]["user"]

        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        if not request.form.get("username"):
            notice = "Must provide a username!"
            return render_template("register.html", notice=notice)

        if not request.form.get("password"):
            notice = "Must provide a password!"
            return render_template("register.html", notice=notice)

        if not request.form.get("confirm"):
            notice = "Must confirm password!"
            return render_template("register.html", notice=notice)

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")

        if password != confirmation:
            notice = "Passwords do not match!"
            return render_template("register.html", notice=notice)

        confirmed_password = generate_password_hash(password)
        user_to_register = [username, confirmed_password]

        conn = sqlite3.connect("math.db")
        db = conn.cursor()
        db.row_factory = sqlite3.Row

        existing_usernames = db.execute("SELECT user FROM users").fetchall()
        for row in existing_usernames:
            if row["user"] == username:
                notice = "Username already exists!"
                return render_template("register.html", notice=notice)

        db.executemany("INSERT INTO users VALUES(?, ?)", [user_to_register])
        conn.commit()
        conn.close()

        return redirect("/login")

    if request.method == "GET":
        return render_template("register.html")

if(__name__ == "__main__"):
    app.run(debug=True)
