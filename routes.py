from flask import Blueprint, render_template, request, redirect, url_for
from models import Exercise, WorkoutExercise, db, User, Plan, Workout
from datetime import datetime

main = Blueprint("main", __name__)

print("ROUTES LOADED")


def parse_optional_date(raw_date):
    if not raw_date:
        return None
    return datetime.strptime(raw_date, "%Y-%m-%d").date()


def parse_optional_int(raw_number):
    if not raw_number:
        return None
    return int(raw_number)


def parse_optional_float(raw_number):
    if not raw_number:
        return None
    return float(raw_number)

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
        

        plan.start_date = parse_optional_date(start_date_raw)
        plan.end_date = parse_optional_date(end_date_raw)


        db.session.commit()
  

    plan = Plan.query.get(plan_id)
    workouts = Workout.query.filter(Workout.plan_id == plan_id).all()
    if not plan:
        return "Plan not found"
    return render_template("viewPlan.html", plan=plan, workouts=workouts)


@main.route("/plans/viewplan/<int:plan_id>/workouts/add", methods=["POST"])
def add_workout_to_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    new_workout = Workout(
        user_id=plan.user_id,
        plan_id=plan.plan_id,
        workout_date=parse_optional_date(request.form.get("workout_date")),
        duration_min=parse_optional_int(request.form.get("duration_min")),
        cals_burned=parse_optional_int(request.form.get("cals_burned")),
        notes=request.form.get("notes") or None,
    )
    db.session.add(new_workout)
    db.session.commit()

    return redirect(url_for("main.view_plan", plan_id=plan.plan_id))


@main.route(
    "/plans/viewplan/<int:plan_id>/workouts/<int:workout_id>/exercises/add",
    methods=["POST"],
)
def add_exercise_to_workout(plan_id, workout_id):
    workout = Workout.query.filter_by(workout_id=workout_id, plan_id=plan_id).first_or_404()
    exercise_name = request.form.get("name", "").strip()

    if not exercise_name:
        return "Exercise name is required"

    exercise = Exercise(
        name=exercise_name,
        muscle_group=request.form.get("muscle_group") or None,
        difficulty=parse_optional_int(request.form.get("difficulty")) or 1,
        equipment_needed=request.form.get("equipment_needed") or None,
    )
    db.session.add(exercise)
    db.session.flush()

    workout_exercise = WorkoutExercise(
        workout_id=workout.workout_id,
        exercise_id=exercise.exercise_id,
        sets_completed=parse_optional_float(request.form.get("sets_completed")),
        reps_completed=parse_optional_float(request.form.get("reps_completed")),
        average_weight=parse_optional_float(request.form.get("average_weight")),
    )
    db.session.add(workout_exercise)
    db.session.commit()

    return redirect(url_for("main.view_plan", plan_id=plan_id))


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
