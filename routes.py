from flask import Blueprint, render_template, request, redirect
from models import db, User

main = Blueprint("main", __name__)

print("ROUTES LOADED")

@main.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@main.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]

    if not name:
        return "Invalid input"

    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")