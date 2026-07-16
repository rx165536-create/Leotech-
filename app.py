from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "leotech_secret_key_2026"

@app.route("/", methods=["GET", "POST"])
def home():
    success = False

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("leotech.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        success = True

    return render_template("index.html", success=success)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "leotech123":
            session["logged_in"] = True
            return redirect("/admin")

    return render_template("login.html")

@app.route("/admin")
def admin():

    if not session.get("logged_in"):
      return redirect("/login")

    conn = sqlite3.connect("leotech.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    messages = cursor.fetchall()

    conn.close()

    return render_template("admin.html", messages=messages)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/login")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("leotech.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)
