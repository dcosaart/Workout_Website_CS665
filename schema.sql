-- Question 2
-- DDL  for a workout tracker app
-- schema, tables, primary keys, foreign keys

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS WorkoutExercises;
DROP TABLE IF EXISTS Workouts;
DROP TABLE IF EXISTS Exercises;
DROP TABLE IF EXISTS Plans;
DROP TABLE IF EXISTS Users;

-- users table 
CREATE TABLE Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    date_joined DATE NOT NULL,
    profile_update DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

-- Plans table 

CREATE TABLE Plans(
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    goal TEXT,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_plans_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


-- Exercises table 
CREATE TABLE Exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL DEFAULT '',
    muscle_group TEXT,
    difficulty INTEGER NOT NULL DEFAULT 1, -- 1 - 5 difficulty lvl
    equipment_needed TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Workouts table 
CREATE TABLE Workouts(
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan_id INTEGER,
    workout_date DATE,
    duration_min INTEGER,
    cals_burned INTEGER,
    notes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_worksouts_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT fk_workouts_plan FOREIGN KEY (plan_id) REFERENCES Plans(plan_id)
);

-- WorkoutExercises table
CREATE TABLE WorkoutExercises(
    workout_exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    sets_completed REAL, 
    reps_completed REAL,
    average_weight REAL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_workoutexercises_workout FOREIGN KEY (workout_id) REFERENCES Workouts(workout_id),
    CONSTRAINT fk_workoutexercises_exercise FOREIGN KEY (exercise_id) REFERENCES Exercises(exercise_id)
);


