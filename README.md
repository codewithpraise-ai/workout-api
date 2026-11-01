# workout-api
Flask SQLAlchemy Workout Application Backend 

# Workout Application Backend API

## Description

The Workout Application Backend is a RESTful API built with Python and Flask. It allows users to manage workouts and exercises, track workout duration, and record exercise details such as repetitions, sets, and duration.

The application uses Flask-SQLAlchemy for database management and Marshmallow for data serialization and validation. SQLite is used as the database.

## Features

* Create, retrieve, and delete workouts.
* Create, retrieve, and delete exercises.
* Add exercises to workouts.
* Track repetitions, sets, and exercise duration.
* Establish many-to-many relationships between workouts and exercises through a WorkoutExercise model.
* Validate incoming data using Marshmallow schemas.
* Enforce database constraints and model-level validations.
* Return appropriate HTTP status codes and error messages.

## Technologies Used

* Python 3.10
* Flask 2.2.2
* Flask-SQLAlchemy 3.0.3
* Flask-Migrate 3.1.0
* Marshmallow 3.20.1
* SQLite
* SQLAlchemy

## Project Structure

```text
workout-api/
│
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   └── migrations/
│
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/codewithpraise-ai/workout-api.git
```

### 2. Navigate into the project

```bash
cd workout-api
```

### 3. Install dependencies

Install Pipenv if it is not already installed:

```bash
pip install pipenv
```

Install the project dependencies:

```bash
pipenv install
```

### 4. Activate the virtual environment

```bash
pipenv shell
```

### 5. Navigate to the server directory

```bash
cd server
```

## Database Setup

The application uses SQLite and Flask-Migrate to manage database migrations.

Set the Flask application:

```bash
export FLASK_APP=app.py
```

Initialize migrations if setting up the database for the first time and the migrations directory does not already exist:

```bash
flask db init
```

Generate a migration:

```bash
flask db migrate -m "Create workout application tables"
```

Apply the migration:

```bash
flask db upgrade
```

## Seeding the Database

To populate the database with sample exercises and workouts, run:

```bash
python seed.py
```

The seed script creates sample exercises and a workout with associated exercises. It checks for existing records to avoid inserting duplicate data when run multiple times.

## Running the Application

From the `server` directory, run:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5555
```

## API Endpoints

All endpoints accept and return JSON unless otherwise specified.

### Exercises

| Method | Endpoint          | Description            |
| ------ | ----------------- | ---------------------- |
| GET    | `/exercises`      | Retrieve all exercises |
| GET    | `/exercises/<id>` | Retrieve one exercise  |
| POST   | `/exercises`      | Create a new exercise  |
| DELETE | `/exercises/<id>` | Delete an exercise     |

Example request to create an exercise:

```json
{
  "name": "Lunges",
  "category": "Strength",
  "equipment_needed": false
}
```

### Workouts

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | `/workouts`      | Retrieve all workouts |
| GET    | `/workouts/<id>` | Retrieve one workout  |
| POST   | `/workouts`      | Create a new workout  |
| DELETE | `/workouts/<id>` | Delete a workout      |

Example request to create a workout:

```json
{
  "date": "2026-11-01",
  "duration_minutes": 30,
  "notes": "Morning workout"
}
```

### Workout Exercises

| Method | Endpoint                                                           | Description                  |
| ------ | ------------------------------------------------------------------ | ---------------------------- |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

Example request:

```json
{
  "reps": 12,
  "sets": 3
}
```

For exercises measured by time, `duration_seconds` can be supplied instead:

```json
{
  "duration_seconds": 60,
  "sets": 3
}
```

## Database Models and Relationships

The application contains three database models:

### Exercise

Stores information about individual exercises.

Fields:

* id
* name
* category
* equipment_needed

### Workout

Stores information about workout sessions.

Fields:

* id
* date
* duration_minutes
* notes

### WorkoutExercise

Acts as the association model connecting workouts and exercises.

Fields:

* id
* workout_id
* exercise_id
* reps
* sets
* duration_seconds

A workout can contain multiple exercises, and an exercise can belong to multiple workouts. The WorkoutExercise model manages this many-to-many relationship.

## Validation

The application uses three levels of validation:

1. **Database constraints:** Enforce rules such as unique exercise names, positive workout durations, and valid exercise measurements.
2. **Model validations:** Use SQLAlchemy validators to prevent invalid values from being assigned to model attributes.
3. **Schema validations:** Use Marshmallow to validate incoming API data, required fields, and positive numerical values.

Invalid requests return appropriate error responses instead of being saved to the database.

## Error Handling

The API uses standard HTTP status codes, including:

* `200 OK` – Successful GET request.
* `201 Created` – Resource successfully created.
* `204 No Content` – Resource successfully deleted.
* `400 Bad Request` – Invalid input or validation error.
* `404 Not Found` – Requested resource does not exist.

## Dependencies

Project dependencies are managed using Pipenv and recorded in the `Pipfile` and `Pipfile.lock`.

Main dependencies include:

* Flask==2.2.2
* Flask-Migrate==3.1.0
* Flask-SQLAlchemy==3.0.3
* Werkzeug==2.2.2
* importlib-metadata==6.0.0
* importlib-resources==5.10.0
* ipdb==0.13.9
* marshmallow==3.20.1

## Author

Developed as a Software Engineering backend development project.
