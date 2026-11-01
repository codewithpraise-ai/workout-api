from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Name cannot be empty.")
    )

    category = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Category cannot be empty.")
    )

    equipment_needed = fields.Boolean(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    reps = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    sets = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def validate_measurement(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError(
                "Provide either reps or duration_seconds."
            )


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.String(allow_none=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )