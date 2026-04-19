from flask import render_template, request, redirect
from app import app
from models import db, User

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]

    if not name:
        return "Invalid input"

    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")