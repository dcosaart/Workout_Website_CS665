from flask import Blueprint, render_template, request, redirect
from models import Exercise, WorkoutExercise, db, User, Plan, Workout
from datetime import datetime

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

@main.route("/plans/viewplan/<int:plan_id>", methods=["GET", "POST"])
def view_plan(plan_id):
    if request.method == "POST":
        name = request.form["name"]
        goal = request.form["goal"]
        description = request.form["description"]
        start_date_raw = request.form.get("start_date")
        end_date_raw = request.form.get("end_date")
    
        if not name or not goal:
            return "Invalid input ..."
    
        plan = Plan.query.get(plan_id)
        if not plan:
            return "Plan not found"
    
        plan.name = name
        plan.goal = goal
        plan.description = description
        

        start_date = None
        end_date = None

        if start_date_raw and start_date_raw!= 'No Start Date':
            start_date = datetime.strptime(start_date_raw, "%Y-%m-%d").date()

        if end_date_raw and end_date_raw != "No End Date":
            end_date = datetime.strptime(end_date_raw, "%Y-%m-%d").date()


        db.session.commit()
  

    plan = Plan.query.get(plan_id)
    workouts = (
        db.session.query(Workout, WorkoutExercise, Exercise)
        .join(WorkoutExercise, Workout.workout_id == WorkoutExercise.workout_id)
        .join(Exercise, WorkoutExercise.exercise_id == Exercise.exercise_id)
        .filter(Workout.plan_id == plan_id)
        .all()
    )
    if not plan:
        return "Plan not found"
    return render_template("viewPlan.html", plan=plan, workouts=workouts)


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

@main.route("/plans/delete/<int:plan_id>", methods=["POST"])
def delete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    db.session.delete(plan)
    db.session.commit()

    return redirect("/plans")