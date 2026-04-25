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

-- Users
INSERT INTO Users (first_name, last_name, email, date_joined) 
VALUES
('Dylan', 'Cossaart', 'djcossaart@wichita.edu', '2026-01-07'),
('John', 'Pork', 'JohnPork@outlook.com', '2025-04-28'),
('Cody', 'Farlow', 'CodyFarlow23@shockers.wichita.edu', '2022-01-01'),
('Ben', 'Gorman', 'BengyGamer123@google.org', '2021-09-09'),
('Addi', 'Nguyen', 'AddiViet67@outlook.com', '2020-04-20');

-- Plans
INSERT INTO Plans (user_id, name, goal, start_date, end_date)
VALUES
(1, 'Running Goal', 'Run a 5k', '2026-01-01', '2026-07-01'),
(2, 'Squat 300', 'Squat 300 for 20 reps', '2022-01-01', '2025-01-01'),
(3, 'Mr. Olympia', 'Retain the Mr.Olympia title', '2020-01-01', NULL),
(4, 'Become jacked', 'Eat protein, get big', '2026-05-01', NULL),
(5, 'Bench 700', 'Bench 700 by May', '2026-01-01', '2026-05-01');

-- Exercises
INSERT INTO Exercises (name, muscle_group, difficulty, equipment_needed)
VALUES
('Bench Press', 'Chest & Tricepts', 4, 'Bench, Barbell'),
('Curls', 'Bicepts', 2, 'Dumbells/Barbell'),
('Shoulder Press', 'Shoulders', 3, 'Bench, Barbell or Dumbells'),
('Squat', 'Quads/Glutes', 5, 'Barbell'),
('Deadlift', 'Hamstrings/Glutes', 5, 'Barbell'),
('Running', 'Cardiovascular', 5, NULL),
('Crunches', 'Core', 1, NULL);

-- Workouts
INSERT INTO Workouts (user_id, plan_id, workout_date, duration_min, cals_burned, notes)
VALUES
(1, 1, '2025-01-01', 30, 200, 'Awesome workout'),
(2, 2, '2026-01-07', 60, 400, 'This sucked, but glad I did it'),
(3, 3, '2026-04-12', 90, 600, 'Very hard workout, nearly vomitted'),
(4, 4, '2026-02-02', 15, 50, 'Quick, easy workout'),
(5, 5, '2025-10-01', 120, 1200, 'Great way to start October');

-- WorkoutExercises
INSERT INTO WorkoutExercises (workout_id, exercise_id, sets_completed, reps_completed, average_weight)
VALUES
(1, 2, 3, 24, 30),
(1, 1, 3, 24, 125),
(2, 3, 3, 24, 200),
(2, 4, 3, 24, 300),
(4, 5, NULL, NULL, NULL),
(5, 1, 5, 100, 200),
(5, 4, 5, 100, 400);

