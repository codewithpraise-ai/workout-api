from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__= 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint('name', name='unique_exercise_name'),
        CheckConstraint("length(trim(name)) > 0", name='exercise_name_not_empty'),
        CheckConstraint("length(trim(category)) > 0", name='exercise_category_not_empty')
    )

    @validates('name', 'category')
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} cannot be empty')

        return value.strip()

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        viewonly=True
    )

    def __repr__(self):
        return f'<Exercise {self.name}>'

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint(
            'duration_minutes > 0',
            name='positive_workout_duration'
        ),
    )

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError('Workout duration must be a positive integer')

        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey('workouts.id'),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id'),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        UniqueConstraint(
            'workout_id',
            'exercise_id',
            name='unique_workout_exercise'
        ),
        CheckConstraint(
            'reps IS NULL OR reps > 0',
            name='positive_reps'
        ),
        CheckConstraint(
            'sets IS NULL OR sets > 0',
            name='positive_sets'
        ),
        CheckConstraint(
            'duration_seconds IS NULL OR duration_seconds > 0',
            name='positive_duration_seconds'
        ),
        CheckConstraint(
            'reps IS NOT NULL OR duration_seconds IS NOT NULL',
            name='exercise_has_measurement'
        )
    )

    workout = db.relationship(
        'Workout',
        back_populates='workout_exercises'
    )

    exercise = db.relationship(
        'Exercise',
        back_populates='workout_exercises'
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_measurements(self, key, value):
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f'{key} must be a positive integer')

        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'
