from flask import Flask, render_template, request, redirect, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import mariadb
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta



load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv("SECRET_KEY", "dev_key")

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7) 

def db_connection():
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    if "user_id" not in session:
        return redirect("/auth")

    if request.method == "POST":
        emne = request.form.get("emne")
        category = request.form.get("category")
        beskrivelse = request.form.get("beskrivelse")

        conn = db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO tickets (user_id, category, emne, beskrivelse) VALUES (?, ?, ?, ?)",
            (session["user_id"], category, emne, beskrivelse)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/") 

    return render_template("kontakt.html")

@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/dashboard")
def dashboard():
    return render_template("drift.html")



@app.route("/signup", methods=["POST"])
def signup():
    session.permanent = True






load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")


def db_connection():
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/auth")
def auth():
    return render_template("auth.html")



@app.route("/signup", methods=["POST"])
def signup():
    first = request.form.get("firstname", "").strip()
    last = request.form.get("lastname", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()

    if not first or not last or not email or not password:
        return "Fyll inn alle feltene", 400

    password_hash = generate_password_hash(password)

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash, role) VALUES (?, ?, ?, ?, 'user')",
            (first, last, email, password_hash)
        )
        conn.commit()

        session["user_email"] = email
        session["user_name"] = first
        session["role"] = "user"

        return redirect("/")

    except mariadb.IntegrityError:
        return "Email finnes allerede", 409

    finally:
        cur.close()
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()

    if not email or not password:
        return "Skriv inn email og passord", 400

    conn = db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, first_name, password_hash, role FROM users WHERE email=?",
        (email,)
    )
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return "Feil email eller passord", 401

    user_id, first_name, password_hash, role = user

    if not check_password_hash(password_hash, password):
        return "Feil email eller passord", 401

    session["user_id"] = user_id
    session["user_email"] = email
    session["user_name"] = first_name
    session["role"] = role

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)



