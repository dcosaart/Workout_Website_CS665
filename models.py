from datetime import date

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    date_joined = db.Column(db.Date, nullable=False, default=date.today)
    profile_update = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    plans = db.relationship("Plan", back_populates="user", cascade="all, delete-orphan")
    workouts = db.relationship("Workout", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, first_name=None, last_name=None, name=None, **kwargs):
        super().__init__(**kwargs)

        # Keep the current route working while matching the schema's split-name columns.
        if name is not None and (first_name is None and last_name is None):
            parts = name.strip().split(maxsplit=1)
            first_name = parts[0] if parts else ""
            last_name = parts[1] if len(parts) > 1 else "Unknown"

        self.first_name = first_name or ""
        self.last_name = last_name or "Unknown"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Plan(db.Model):
    __tablename__ = "Plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    user = db.relationship("User", back_populates="plans")
    workouts = db.relationship("Workout", back_populates="plan")


class Exercise(db.Model):
    __tablename__ = "Exercises"

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default="")
    muscle_group = db.Column(db.Text)
    difficulty = db.Column(db.Integer, nullable=False, default=1)
    equipment_needed = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")


class Workout(db.Model):
    __tablename__ = "Workouts"

    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    plan_id = db.Column(db.Integer, db.ForeignKey("Plans.plan_id"))
    workout_date = db.Column(db.Date)
    duration_min = db.Column(db.Integer)
    cals_burned = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    user = db.relationship("User", back_populates="workouts")
    plan = db.relationship("Plan", back_populates="workouts")
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(db.Model):
    __tablename__ = "WorkoutExercises"

    workout_exercise_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("Workouts.workout_id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("Exercises.exercise_id"), nullable=False)
    sets_completed = db.Column(db.Float)
    reps_completed = db.Column(db.Float)
    average_weight = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")
