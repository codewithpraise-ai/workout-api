#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # Create sample exercises if they don't already exist
    exercises_data = [
        {
            "name": "Push-ups",
            "category": "Strength",
            "equipment_needed": False
        },
        {
            "name": "Squats",
            "category": "Strength",
            "equipment_needed": False
        },
        {
            "name": "Treadmill Running",
            "category": "Cardio",
            "equipment_needed": True
        },
        {
            "name": "Plank",
            "category": "Core",
            "equipment_needed": False
        }
    ]

    exercises = {}

    for data in exercises_data:
        exercise = Exercise.query.filter_by(name=data["name"]).first()

        if not exercise:
            exercise = Exercise(**data)
            db.session.add(exercise)

        exercises[data["name"]] = exercise

    db.session.flush()

    # Create a sample workout if it doesn't already exist
    workout = Workout.query.filter_by(
        date=date(2026, 10, 31),
        notes="Full body workout"
    ).first()

    if not workout:
        workout = Workout(
            date=date(2026, 10, 31),
            duration_minutes=45,
            notes="Full body workout"
        )
        db.session.add(workout)
        db.session.flush()

    # Connect exercises to the workout
    workout_exercises_data = [
        {
            "exercise": exercises["Push-ups"],
            "reps": 15,
            "sets": 3
        },
        {
            "exercise": exercises["Squats"],
            "reps": 20,
            "sets": 3
        },
        {
            "exercise": exercises["Treadmill Running"],
            "duration_seconds": 600,
            "sets": 1
        },
        {
            "exercise": exercises["Plank"],
            "duration_seconds": 60,
            "sets": 3
        }
    ]

    for data in workout_exercises_data:
        existing = WorkoutExercise.query.filter_by(
            workout_id=workout.id,
            exercise_id=data["exercise"].id
        ).first()

        if not existing:
            workout_exercise = WorkoutExercise(
                workout=workout,
                **data
            )
            db.session.add(workout_exercise)

    db.session.commit()

    print("Database seeded successfully!")
    