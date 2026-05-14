# Normalization Report

## Original Functional Dependencies

The workout tracker database stores users, workout plans, workouts, exercises, and the exercises completed during a workout. Based on the starting schema, the main functional dependencies are:

- `user_id -> first_name, last_name, email, date_joined, profile_update`
- `plan_id -> user_id, name, goal, description, start_date, end_date, created_at, updated_at`
- `exercise_id -> name, muscle_group, difficulty, equipment_needed, created_at, updated_at`
- `workout_id -> user_id, plan_id, workout_date, duration_min, cals_burned, notes, created_at, updated_at`
- `workout_exercise_id -> workout_id, exercise_id, sets_completed, reps_completed, average_weight, created_at, updated_at`

There is also an implied relationship where a user can own many plans and workouts, a plan can contain many workouts, and a workout can contain many exercises. Since the same exercise can appear in many workouts, the relationship between workouts and exercises is many-to-many and requires a junction table.

## Anomaly Identification

If workout, plan, user, and exercise data were stored together in one large table, several anomalies would occur.

An update anomaly could happen if user information or exercise information appeared in many rows. For example, if the name or equipment for “Bench Press” needed to change, every workout row containing Bench Press would need to be updated. Missing one row would cause inconsistent data.

An insertion anomaly could happen if the database required workout information before allowing an exercise or user to be added. For example, a new exercise could not be stored unless it was already attached to a workout. Similarly, a user might not be insertable unless they already had a plan or workout.

A deletion anomaly could happen if deleting a workout also accidentally removed the only stored copy of an exercise or user-related information. For example, deleting the last workout that used “Crunches” could remove the only record showing that the exercise exists.

The original unnormalized structure would also repeat plan, user, and exercise data across multiple workout rows. This redundancy increases storage needs and makes the database harder to maintain.

## Decomposition Steps

To reach Third Normal Form, the schema is decomposed so that each table describes one main entity and every non-key attribute depends only on that table’s primary key.

First, user data is separated into a `Users` table. This removes repeated user names and emails from plan or workout records.

Second, plan data is separated into a `Plans` table. Each plan belongs to one user through `user_id`, but plan-specific fields such as `name`, `goal`, `description`, `start_date`, and `end_date` depend only on `plan_id`.

Third, exercise data is separated into an `Exercises` table. Exercise attributes such as `muscle_group`, `difficulty`, and `equipment_needed` depend only on `exercise_id`, not on a workout.

Fourth, workout data is separated into a `Workouts` table. Each workout can reference both a user and a plan, while workout-specific attributes such as date, duration, calories burned, and notes depend only on `workout_id`.

Finally, the many-to-many relationship between workouts and exercises is decomposed into `WorkoutExercises`. This table connects one workout to one exercise and stores completion-specific data such as sets, reps, and average weight. These values belong to the workout-exercise event, not to the exercise itself.

## Final Relational Schema

The Python application uses the following normalized schema:

- `Users(user_id, first_name, last_name, email, date_joined, profile_update)`
- `Plans(plan_id, user_id, name, goal, description, start_date, end_date, created_at, updated_at)`
- `Exercises(exercise_id, name, muscle_group, difficulty, equipment_needed, created_at, updated_at)`
- `Workouts(workout_id, user_id, plan_id, workout_date, duration_min, cals_burned, notes, created_at, updated_at)`
- `WorkoutExercises(workout_exercise_id, workout_id, exercise_id, sets_completed, reps_completed, average_weight, created_at, updated_at)`

Foreign key relationships:

- `Plans.user_id` references `Users.user_id`
- `Workouts.user_id` references `Users.user_id`
- `Workouts.plan_id` references `Plans.plan_id`
- `WorkoutExercises.workout_id` references `Workouts.workout_id`
- `WorkoutExercises.exercise_id` references `Exercises.exercise_id`

This final structure satisfies 3NF because each table has a primary key, each non-key attribute depends on the whole key, and there are no transitive dependencies between non-key attributes. The design also avoids unnecessary duplication and reduces update, insertion, and deletion anomalies.
