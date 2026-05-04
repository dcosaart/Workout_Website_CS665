from flask import Blueprint, render_template, request, redirect
from models import db, User, Plan, Workout

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

@main.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@main.route("/plans", methods=["GET"])
def get_plans():
    plans_query = db.session.query(Plan, User).join(User, Plan.user_id == User.user_id).all()

    plans = []

    for plan, user in plans_query:
        plans.append({
            "plan_id": plan.plan_id,
            "user_id": user.user_id,
            "user_name": user.name,
            "name": plan.name,
            "goal": plan.goal
        })

    return render_template("plans.html", plans=plans)


@main.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return render_template("workouts.html", workouts=workouts)

@main.route("/plans/viewplan/<int:plan_id>", methods=["GET"])
def view_plan(plan_id):
    plan = Plan.query.get(plan_id)
    if not plan:
        return "Plan not found"
    return render_template("viewPlan.html", plan=plan)

@main.route("/plans/add", methods=["GET", "POST"])
def add_plan():
    if request.method == "POST":
        name = request.form["name"]
        goal = request.form["goal"]
     
        user_id = request.form["user_id"]
        
     

        if not name or not goal or not user_id:
            return "Invalid input ..."

        new_plan = Plan(name=name, goal=goal, user_id=user_id)
        db.session.add(new_plan)
        db.session.commit()

        return redirect("/plans")

    users = User.query.all()
    return render_template("create/addPlan.html", users=users)