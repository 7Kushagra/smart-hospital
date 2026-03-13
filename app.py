from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "smart_hospital_secret"


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# HOME PAGE (Dashboard)
# -----------------------------
@app.route("/")
def home():

    announcements = [
        "Hospital OPD will remain closed on Sunday except emergency services. / रविवार को ओपीडी बंद रहेगी।",
        "Free Health Checkup Camp on 25 March. / 25 मार्च को मुफ्त स्वास्थ्य जांच शिविर।",
        "New MRI Machine installed on Floor 2 Block A. / नई MRI मशीन फ्लोर 2 ब्लॉक A में स्थापित।",
        "Blood Donation Camp this Saturday. / इस शनिवार रक्तदान शिविर।",
        "Covid Booster Vaccination available daily. / कोविड बूस्टर टीकाकरण प्रतिदिन उपलब्ध।",
        "Patient visiting hours: 4PM – 7PM. / मरीजों से मिलने का समय 4PM – 7PM।"
    ]

    return render_template("index.html", announcements=announcements)


# -----------------------------
# DOCTORS PAGE
# -----------------------------
@app.route("/doctors")
def doctors():

    department = request.args.get("department")

    db = get_db()

    if department:
        doctors = db.execute(
            "SELECT * FROM doctors WHERE department=?",
            (department,)
        ).fetchall()
    else:
        doctors = db.execute(
            "SELECT * FROM doctors"
        ).fetchall()

    departments = db.execute(
        "SELECT DISTINCT department FROM doctors"
    ).fetchall()

    return render_template(
        "doctors.html",
        doctors=doctors,
        departments=departments
    )


# -----------------------------
# DEPARTMENTS PAGE
# -----------------------------
@app.route("/departments")
def departments():

    db = get_db()
    departments = db.execute("SELECT * FROM departments").fetchall()

    return render_template("departments.html", departments=departments)


# -----------------------------
# FACILITIES PAGE
# -----------------------------
@app.route("/facilities")
def facilities():
    return render_template("facilities.html")


# -----------------------------
# ANNOUNCEMENTS PAGE
# -----------------------------
@app.route("/announcements")
def announcements():

    announcements = [
        {
            "title": "Hospital Closed Sunday",
            "message": "OPD will remain closed on Sunday except emergency services.",
            "date": "20 March 2026"
        },
        {
            "title": "Free Health Camp",
            "message": "Free health checkup camp on 25 March.",
            "date": "25 March 2026"
        },
        {
            "title": "New MRI Machine",
            "message": "New MRI scanner installed in Block A Floor 2.",
            "date": "18 March 2026"
        },
        {
            "title": "Blood Donation Camp",
            "message": "Blood donation camp this Saturday.",
            "date": "22 March 2026"
        },
        {
            "title": "Covid Vaccination",
            "message": "Covid booster vaccination available daily.",
            "date": "Daily"
        }
    ]

    return render_template("announcements.html", announcements=announcements)


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        role = request.form.get("role")
        password = request.form.get("password")

        if role == "admin":

            if password == "admin123":

                session["admin"] = True
                return redirect("/admin")

            else:
                return "Wrong admin password"

        if role == "patient":
            return redirect("/")

    return render_template("login.html")


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    db = get_db()
    doctors = db.execute("SELECT * FROM doctors").fetchall()

    return render_template("admin.html", doctors=doctors)


# -----------------------------
# ADD DOCTOR
# -----------------------------
@app.route("/add_doctor", methods=["GET","POST"])
def add_doctor():

    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":

        admin_pass = request.form.get("admin_pass")

        if admin_pass != "admin123":
            return "Wrong Admin Password"

        name = request.form["name"]
        department = request.form["department"]
        speciality = request.form["speciality"]
        room = request.form["room"]
        days = request.form["days"]
        time = request.form["time"]

        db = get_db()

        db.execute(
        "INSERT INTO doctors (name,department,speciality,room,days,time) VALUES (?,?,?,?,?,?)",
        (name,department,speciality,room,days,time)
        )

        db.commit()

        return redirect("/admin")

    return render_template("add_doctor.html")


# -----------------------------
# DELETE DOCTOR
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):

    if not session.get("admin"):
        return redirect("/login")

    db = get_db()

    db.execute("DELETE FROM doctors WHERE id=?", (id,))
    db.commit()

    return redirect("/admin")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# -----------------------------
# CHATBOT (Hindi + English)
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    message = data.get("message").lower()

    if "mri" in message or "एमआरआई" in message:
        reply = "MRI Department is on Floor 2, Room 220. / एमआरआई विभाग फ्लोर 2, कमरा 220 में है।"

    elif "blood" in message or "ब्लड" in message:
        reply = "Blood Bank is on Floor 1, Room 105 near ICU. / ब्लड बैंक फ्लोर 1, कमरा 105 में है।"

    elif "cardiology" in message or "दिल" in message:
        reply = "Cardiology doctors are available in Rooms 201–205. / कार्डियोलॉजी डॉक्टर कमरा 201–205 में उपलब्ध हैं।"

    elif "cafeteria" in message or "कैफेटेरिया" in message:
        reply = "Cafeteria is on the ground floor. / कैफेटेरिया ग्राउंड फ्लोर पर है।"

    else:
        reply = "Ask about MRI, Blood Bank, Cafeteria etc. / आप MRI, ब्लड बैंक या कैफेटेरिया के बारे में पूछ सकते हैं।"

    return {"reply": reply}

# Emergency Page
@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5005)
    